import pandas as pd
from urlextract import URLExtract
from collections import Counter
import emojis

extract = URLExtract()


def fetch_stats(selected_user, df):
    if selected_user == 'Overall':
        # fetch no. of messages
        num_messages = df.shape[0]
        # fetch no. of words
        words = []
        for message in df['wp_message']:
            words.extend(message.split())
        # fetch no. of media
        num_media = df[df['wp_message'] == '<Media omitted>\n'].shape[0]

        # fetch the links shared
        links = []
        for message in df['wp_message']:
            urls = extract.find_urls(message)
            links.extend(urls)

        return num_messages, len(words), num_media, len(links)
    else:
        new_df = df[df['wp_user'] == selected_user]
        num_messages = new_df.shape[0]

        words = []
        for message in new_df['wp_message']:
            words.extend(message.split())
        num_media = new_df[new_df['wp_message'] == '<Media omitted>\n'].shape[0]

        links = []
        for message in new_df['wp_message']:
            urls = extract.find_urls(message)
            links.extend(urls)

        return num_messages, len(words), num_media, len(links)


def most_busy_users(df):
    x = df['wp_user'].value_counts().head(5)
    return x


def most_common_words(selected_user, df):
    f = open('stop_hinglish.txt', 'r')
    stopwords = f.read()

    if selected_user != 'Overall':
        df = df[df['wp_user'] == selected_user]

    temp = df[df['wp_user'] != 'group_notification']
    temp = temp[temp['wp_message'] != '<Media omitted>\n']

    words = []
    for message in temp['wp_message']:
        for word in message.lower().split():
            if word not in stopwords:
                words.append(word)

    return_df = pd.DataFrame(Counter(words).most_common(20))
    return return_df


def emoji(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['wp_user'] == selected_user]

    emoji_list = []
    for message in df['wp_message']:
        emoji_list.extend(emojis.get(message))

    emoji_df = pd.DataFrame(Counter(emoji_list).most_common(len(Counter(emoji_list))))
    return emoji_df


def monthly_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['wp_user'] == selected_user]

    timeline = df.groupby(['year', 'month_name', 'month']).count()['wp_message'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))

    timeline['time'] = time

    return timeline


def week_activity_map(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['wp_user'] == selected_user]

    return df['day_name'].value_counts()


def month_activity_map(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['wp_user'] == selected_user]

    return df['month'].value_counts()


def activity_heatmap(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['wp_user'] == selected_user]

    user_heatmap = df.pivot_table(index='day_name', columns='period', values='wp_message', aggfunc='count').fillna(0)

    return user_heatmap
