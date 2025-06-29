import streamlit as st
import google.generativeai as genai

genai.configure(api_key="Enter your API key")


system_prompt=[

   """ You are a domain expert in medical image analysis. You are tasked with examining medical images for a renowned hospital. 
   Your expertise will help in identifying or discovering any anomalies, diseases, conditions or any health issues that might be present in the image.

Your key responsibilities:

Detailed Analysis: Scrutinize and thoroughly examine each image, focusing on finding any abnormalities.

Analysis Report: Document all the findings and clearly articulate them in a structured format.

Recommendations: Basis the analysis, suggest remedies, tests or treatments as applicable.

Treatments: If applicable, lay out detailed treatments which can help in faster recovery.

Important Notes to remember:

Scope of response: Only respond if the image pertains to human health issues.

Clarity of image: In case the image is unclear, note that certain aspects are "Unable to be correctly determined based on the uploaded image."

Disclaimer: Accompany your analysis with the disclaimer: "Consult with a Doctor before making any decisions."

*Your insights are invaluable in guiding clinical decisions. Please proceed with the analysis, adhering to the structured approach outlined above.

Please provide the final response with these 4 headings: Detailed Analysis, Analysis Report, Recommendations and Treatments """

]

model=genai.GenerativeModel(model_name="gemini-1.5-flash")
st.set_page_config(page_title="AI Medical Report Generator", layout="centered")
st.title("🧠 AI-Powered Medical Report Generator (Gemini)")
st.markdown("Generate structured medical insights from symptoms and lab data. *(Not a substitute for medical advice.)*")

file_uploaded=st.file_uploader('Upload the image for analysis', type=['jpg','png','jpeg','jfif'])
if file_uploaded:
    st.image(file_uploaded,width=200, caption='Upload Image')

submit=st.button("Generate Analysis")

if submit:
    image_data=file_uploaded.getvalue()

    image_parts=[
        {
            "mime_type": "image/jpeg",
            "data" :image_data
        }
    ]
    prompt_parts=[
        image_parts[0],
        system_prompt[0],
    ]

    try:
        response = model.generate_content(prompt_parts)
        if response:
            st.subheader("📜 AI Medical Analysis Report")
            st.write(response.text)

            # ✅ Download button
            st.download_button(
                label="📥 Download Report",
                data=response.text,
                file_name="medical_analysis_report.txt",
                mime="text/plain"
            )
    except Exception as e:
        st.error(f"❌ Failed to generate report: {e}")

        