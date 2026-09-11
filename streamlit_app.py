import streamlit as st
from pipeline import process_submission

st.set_page_config(
    page_title="SamadhanHub AI",
    page_icon="🏛️",
    layout="centered"
)

st.title("🏛️ SamadhanHub AI Service")
st.markdown("Submit a societal challenge and see how the AI processes it through all 5 stages.")

st.divider()

submission_id = st.text_input("Submission ID", value="SUB001")
text = st.text_area(
    "Complaint / Challenge Text",
    height=150,
    placeholder="Example: The water pipeline in our village has been broken for two weeks..."
)

if st.button("Process Submission", type="primary"):
    if not text.strip():
        st.warning("Please enter some text.")
    else:
        with st.spinner("Running through AI pipeline..."):
            result = process_submission(submission_id, text)

        st.divider()
        st.subheader("Result")

        if result["is_valid"]:
            st.success("✅ Valid Submission")
        else:
            st.error("❌ Invalid / Junk Submission")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown(f"**Submission ID:** `{result['submission_id']}`")
            st.markdown(f"**Valid:** `{result['is_valid']}`")
            st.markdown(f"**Category:** `{result.get('category')}`")
            # Surface the model's confidence so low-confidence guesses
            # are visible instead of looking as certain as a clean match
            # NOTE: pipeline.py returns "domain_match_score" (0-100) and
            # "low_confidence" (bool) -- earlier keys here never matched
            # what pipeline.py actually returns, so this block never fired.
            if result.get("domain_match_score") is not None:
                st.markdown(f"**Category confidence:** `{result['domain_match_score']}/100`")
                if result.get("low_confidence"):
                    st.warning("⚠️ Low confidence category — may need manual review.")

        with col2:
            st.markdown(f"**Priority:** `{result.get('priority')}`")
            st.markdown(f"**Duplicate:** `{result.get('is_duplicate')}`")
            if result.get("duplicate_of"):
                st.markdown(f"**Duplicate of:** `{result['duplicate_of']}`")

        st.markdown(f"**Matched Department:** `{result.get('matched_department')}`")

        with st.expander("View Full JSON Response"):
            st.json(result)

st.divider()
st.caption("Stages: Validation → Classification → Deduplication → Priority → University Match")