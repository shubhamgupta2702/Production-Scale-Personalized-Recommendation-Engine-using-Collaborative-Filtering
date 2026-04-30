import streamlit as st
import requests
import traceback


API_URL = "http://127.0.0.1:8000"



st.set_page_config(
    page_title="Book Recommender System",
    page_icon="📚",
    layout="wide"
)


@st.cache_data
def fetch_books():
    try:
        response = requests.get(
            f"{API_URL}/books"
        )

        response.raise_for_status()

        return response.json()["books"]

    except Exception as e:
        st.error(
            f"Failed to fetch books: {e}"
        )
        return []


def fetch_recommendations(
    book_name,
    top_n=5
):
    try:
        payload = {
            "book_name": book_name,
            "top_n": top_n
        }

        response = requests.post(
            f"{API_URL}/recommend",
            json=payload
        )

        response.raise_for_status()

        return response.json()

    except Exception as e:
        st.error(
            f"Recommendation failed: {e}"
        )
        return None


def main():
    try:
        st.title(
            "📚 Personalized Book Recommender"
        )

        st.write(
            "Find books similar to your favorite books"
        )

        books = fetch_books()

        if not books:
            st.warning(
                "No books found."
            )
            return

        selected_book = st.selectbox(
            "Select a book",
            books
        )

        top_n = st.slider(
            "Number of recommendations",
            min_value=1,
            max_value=10,
            value=5
        )

        if st.button("Recommend"):
            with st.spinner(
                "Finding recommendations..."
            ):
                result = fetch_recommendations(
                    selected_book,
                    top_n
                )

                if result:
                    recommendations = result[
                        "recommendations"
                    ]

                    st.subheader(
                        "Recommended Books"
                    )

                    cols = st.columns(
                        len(recommendations)
                    )

                    for idx, book in enumerate(
                        recommendations
                    ):
                        with cols[idx]:
                            st.image(
                                book["image_url"],
                                use_container_width=True
                            )

                            st.write(
                                f"**{book['title']}**"
                            )

                            st.caption(
                                book["author"]
                            )

                    st.success(
                        f"Response time: "
                        f"{result['latency']} ms"
                    )

    except Exception as e:
        st.error(
            "Application failed."
        )

        st.error(str(e))

        st.code(
            traceback.format_exc()
        )

if __name__ == "__main__":
    main()