import requests
import os
import pandas as pd
import plotly.graph_objects as go
import numpy as np


class Integration:
    def __init__(self, username):
        if not isinstance(username, str):
            raise ValueError("Username must be a string")
        self.username = username
        self._bearer_token = os.environ.get("TWITTER_BEARER_TOKEN")
        self.user_id = self._get_id_from_username()

    def _bearer_oauth(self, r, user_agent):
        """
        Method required by bearer token authentication.
        """

        r.headers["Authorization"] = f"Bearer {self._bearer_token}"
        r.headers["User-Agent"] = user_agent
        return r

    def _connect_to_endpoint(self, url, user_agent, params):
        response = requests.request(
            "GET",
            url,
            auth=lambda r: self._bearer_oauth(r, user_agent),
            params=params,
        )
        if response.status_code != 200:
            raise Exception(
                f"Request returned an error: {response.status_code}"
                f"{response.text}"
            )

        return response.json()

    def _get_params(self, max_results):
        return {
            "max_results": max_results,
            "tweet.fields": "created_at,public_metrics,author_id",
        }

    def _get_id_from_username(self):
        url = f"https://api.twitter.com/2/users/by?usernames={self.username}"
        json_response = self._connect_to_endpoint(
            url=url, user_agent="v2UserLookupPython", params=""
        )

        # TODO: Make some kind of try-except here,
        # TODO: to check if the user actually exists

        id = json_response["data"][0]["id"]
        return id

    # TODO: Allow pagination
    def _get_user_timeline(self, max_results):
        url = f"https://api.twitter.com/2/users/{self.user_id}/tweets"
        params = self._get_params(max_results)
        json_response = self._connect_to_endpoint(
            url=url, user_agent="v2UserTweetsPython", params=params
        )

        return json_response

    # TODO: Allow pagination
    def _get_mentions_timeline(self, max_results):
        url = f"https://api.twitter.com/2/users/{self.user_id}/mentions"
        params = self._get_params(max_results)
        json_response = self._connect_to_endpoint(
            url=url, user_agent="v2UserMentionsPython", params=params
        )

        return json_response

    def get_tweet_table(self, max_results, type: str):
        # TODO: Use enum https://realpython.com/python-enum/
        if type not in ["user", "mentions"]:
            raise ValueError("Type must be 'user' or 'mentions'")

        if type == "user":
            json_response = self._get_user_timeline(max_results=max_results)

        if type == "mentions":
            json_response = self._get_mentions_timeline(
                max_results=max_results
            )

        id = []
        created_at = []
        text = []
        retweet_count = []
        reply_count = []
        like_count = []
        quote_count = []
        bookmark_count = []
        impression_count = []
        author_id = []

        if isinstance(json_response, dict):
            for i in json_response["data"]:
                author_id.append(i["author_id"])
                id.append(i["id"])
                created_at.append(i["created_at"])
                text.append(i["text"])
                retweet_count.append(i["public_metrics"]["retweet_count"])
                reply_count.append(i["public_metrics"]["reply_count"])
                like_count.append(i["public_metrics"]["like_count"])
                quote_count.append(i["public_metrics"]["quote_count"])
                bookmark_count.append(i["public_metrics"]["bookmark_count"])
                impression_count.append(
                    i["public_metrics"]["impression_count"]
                )

        df = pd.DataFrame()
        df["id"] = id
        df["author_id"] = author_id
        df["created_at"] = created_at
        df["Publiceringsdato"] = df["created_at"].str.split("T").str[0]
        df["Tekst"] = text
        df["Retweets"] = retweet_count
        df["Replies"] = reply_count
        df["Likes"] = like_count
        df["Citeringer"] = quote_count
        df["Bogmarkeringer"] = bookmark_count
        df["Impressions"] = impression_count
        df["Popularitet"] = (
            df["Retweets"]
            + df["Replies"]
            + df["Likes"]
            + df["Citeringer"]
            + df["Bogmarkeringer"]
        )

        # return df
        if type == "user":
            self.user_tweet_table = df

        if type == "mentions":
            self.mentions_tweet_table = df

    def visualize_popularity(self, df):
        df["Publiceringsdato"] = df["Publiceringsdato"].astype(str)
        fig = go.Figure()

        # Original scatter plot
        fig.add_trace(
            go.Scatter(
                x=df["Publiceringsdato"],  # date/time data for the x-axis
                y=df["Popularitet"],  # polarity scores for the y-axis
                mode="markers",  # scatter plot
                name="Popularitet",  # name of the trace
                text=df.index,
                hoverinfo="text",
                marker=dict(
                    size=10,
                    color=df["Popularitet"],  # set color to polarity score
                    colorscale="RdYlGn",  # choose a colorscale
                    reversescale=False,  # reverse to have green at top
                    #                    colorbar=dict(
                    #                        title="Popularity Score",
                    #                    ),
                ),
            )
        )

        # Add a trendline
        z = np.polyfit(
            range(len(df["Publiceringsdato"])), df["Popularitet"], 1
        )
        p = np.poly1d(z)
        fig.add_trace(
            go.Scatter(
                x=df["Publiceringsdato"],
                y=p(range(len(df["Publiceringsdato"]))),
                mode="lines",
                name="Trendline",
                line=dict(color="grey"),
            )
        )

        fig.update_layout(
            title="Popularitet over tid",
            xaxis_title="Tid",
            yaxis_title="Popularitet",
            # xaxis=dict(
            #     tickmode="linear",
            #     dtick="86400000",  # One day in milliseconds
            # ),
        )

        return fig

    def _get_tweet_url(self, post_id):
        return f"https://twitter.com/{self.username}/status/{post_id}"

    def _get_posts_as_embeded(self, type) -> None:
        """
        Retrieves posts as embedded HTML from Twitter based on the given type.

        To show in streamlit:
            import streamlit.components.v1 as components
            components.html(res, height=800)
        """

        if type == "user":
            if self.user_tweet_table is not None:
                ids = self.user_tweet_table["id"]

                results = []
                for id in ids:
                    url = self._get_tweet_url(id)
                    api = f"https://publish.twitter.com/oembed?url={url}"
                    response = requests.get(api)
                    results.append(response.json()["html"])

                return results


if __name__ == "__main__":
    import streamlit as st
    import streamlit.components.v1 as components

    st.set_page_config(
        page_title=None,
        page_icon=None,
        layout="wide",
        initial_sidebar_state="auto",
        menu_items=None,
    )

    riri = Integration("rihanna")
    riri.get_tweet_table(5, "user")
    results = riri._get_posts_as_embeded(type="user")

    col1, col2, col3 = st.columns(3, gap="large")

    if results is not None:
        with col1:
            st.header("A cat")
            components.html(results[0], height=800)

        with col2:
            st.header("A dog")
            components.html(results[1], height=800)

        with col3:
            st.header("An owl")
            components.html(results[2], height=800)

    # riri.get_post_as_embeded()
