import streamlit as st
import preprocessor
import helper
import matplotlib.pyplot as plt
import seaborn as sns

st.sidebar.title('Whatsapp Chat Analyzer')

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)

    # fetch unique users
    user_list = df['wp_user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0, 'Overall')

    selected_user = st.sidebar.selectbox('Show analysis with respect to', user_list)

    if st.sidebar.button("Show Analysis"):

        num_messages, words, num_media, num_links = helper.fetch_stats(selected_user, df)

        st.title('Top Statistics')

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.header("Total Messages")
            st.title(num_messages)
        with col2:
            st.header("Total Words")
            st.title(words)
        with col3:
            st.header("Media Shared")
            st.title(num_media)
        with col4:
            st.header("Links Shared")
            st.title(num_links)

        # timeline
        st.title('Monthly Timeline')

        timeline = helper.monthly_timeline(selected_user, df)
        fig1, ax1 = plt.subplots()

        ax1.plot(timeline['time'], timeline['wp_message'], color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig1)

        # activity map
        st.title('Activity Map')
        col7, col8 = st.columns(2)

        with col7:
            st.header('Most Busy Day')
            busy_day = helper.week_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values)
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col8:
            st.header('Most Busy Month')
            busy_month = helper.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values, color='orange')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        st.title("Weekly Activity Map")
        user_heatmap = helper.activity_heatmap(selected_user, df)
        fig, ax = plt.subplots()
        ax = sns.heatmap(user_heatmap)
        st.pyplot(fig)

        if selected_user == 'Overall':
            st.title('Most Busy Users')
            x = helper.most_busy_users(df)
            fig2, ax2 = plt.subplots()

            ax2.barh(x.index, x.values)
            plt.xticks(rotation='vertical')
            st.pyplot(fig2)

        # Most Common Words

        st.title('Most Common Words')
        return_df = helper.most_common_words(selected_user, df)

        fig3, ax3 = plt.subplots()

        ax3.barh(return_df[0], return_df[1])
        plt.xticks(rotation='vertical')
        st.pyplot(fig3)

        # Emojis
        st.title('Emoji Analysis')

        emoji_df = helper.emoji(selected_user, df)

        col5, col6 = st.columns(2)

        with col5:
            st.dataframe(emoji_df)
        with col6:
            fig4, ax4 = plt.subplots()
            ax4.barh(emoji_df[0], emoji_df[1])
            st.pyplot(fig4)
