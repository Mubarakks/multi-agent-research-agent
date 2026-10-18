import streamlit as st
from pipeline import Base_research_pipeline

st.set_page_config(
    page_title="MagentaAI | Research Assistant",
    page_icon="🔎",
    layout="wide",
)


st.markdown(
    """
    <style>
      .stApp { background: #10131a; color: #f2f4f8; }
      .block-container { padding-top: 2rem; max-width: 1200px; }
      .hero {
        padding: 1.6rem 1.8rem;
        border: 1px solid rgba(150,160,190,.25);
        border-radius: 18px;
        background: linear-gradient(135deg, #1d2433, #151923);
        margin-bottom: 1.4rem;
      }
      .hero h1 { margin: 0; font-size: 2.25rem; }
      .hero p { color: #b8c1d4; margin-bottom: 0; }
      div[data-testid="stExpander"] { border-radius: 12px; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="hero">
      <h1>🔎 MagentaAI</h1>
      <p>Multi-agent research assistant · Search, read, write, and review</p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.write(
    "Enter a topic below. MagentaAI will run your existing pipeline: "
    "Search Agent → Reader Agent → Writer → Critic."
)

with st.form("research_form"):
    topic = st.text_input(
        "Research topic",
        placeholder="e.g., Recent advances in renewable energy in India",
    )
    submitted = st.form_submit_button("🚀 Start research", use_container_width=True)

if submitted:
    if not topic.strip():
        st.warning("Please enter a research topic first.")
    else:
        try:
            with st.status("Research is running. This may take a little while...", expanded=True) as status:
                st.write("Running Search Agent, Reader Agent, Writer, and Critic...")
                # The pipeline currently prints progress in the terminal and returns
                # each stage's result in a dictionary.
                result = Base_research_pipeline(topic.strip())
                status.update(label="Research completed", state="complete", expanded=False)

            st.success("Research completed successfully.")

            search_results = result.get("search_results", "")
            scraped_content = result.get("scraped_content", "")
            report = result.get("report", "")
            feedback = result.get("feedback", "")

            tab_report, tab_search, tab_reader, tab_critic = st.tabs(
                ["📄 Final report", "🌐 Search results", "📚 Scraped content", "🧐 Critic feedback"]
            )

            with tab_report:
                st.subheader("Final research report")
                if report:
                    st.markdown(str(report))
                    st.download_button(
                        "⬇️ Download report as text",
                        data=str(report),
                        file_name="magentaai_research_report.txt",
                        mime="text/plain",
                    )
                else:
                    st.info("The pipeline did not return a report.")

            with tab_search:
                st.subheader("Search Agent output")
                st.write(search_results or "No search results were returned.")

            with tab_reader:
                st.subheader("Reader Agent output")
                st.write(scraped_content or "No scraped content was returned.")

            with tab_critic:
                st.subheader("Critic feedback")
                st.write(feedback or "No critic feedback was returned.")

            with st.expander("Show complete pipeline output"):
                st.json(
                    {
                        "search_results": search_results,
                        "scraped_content": scraped_content,
                        "report": report,
                        "feedback": feedback,
                    }
                )

        except Exception as exc:
            st.error("The research pipeline failed.")
            st.exception(exc)
            st.info(
                "If the error mentions a missing key, check your .env file. "
                "If it mentions a Python syntax error, fix pipeline.py first."
            )

st.caption("MagentaAI · Your research workflow, in one place")
