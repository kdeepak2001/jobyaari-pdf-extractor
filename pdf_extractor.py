# JobYaari PDF Job Extractor
# Built for JobYaari Internship Application

import PyPDF2
from openai import OpenAI

print("=" * 60)
print("       JobYaari PDF Job Extractor")
print("    Powered by FREE Google Gemini AI")
print("=" * 60)

# Setup FREE Gemini API
print("\n🔧 Connecting to Gemini AI...")
client = OpenAI(
    api_key="YOUR_GEMINI_API_KEY_HERE",
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)
print("✅ Connected to Gemini AI successfully!")

def extract_pdf_text(pdf_path):
    """Read text from PDF file"""
    print(f"\n📄 Opening PDF: {pdf_path}")
    
    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ""
            total_pages = len(reader.pages)
            
            print(f"📖 Total pages in PDF: {total_pages}")
            print("🔍 Extracting text from all pages...")
            
            for page_num in range(total_pages):
                page = reader.pages[page_num]
                text += page.extract_text()
                print(f"   ✓ Processed page {page_num + 1}/{total_pages}")
            
            print(f"\n✅ Extracted {len(text)} characters from PDF")
            return text
    
    except FileNotFoundError:
        print(f"\n❌ ERROR: File '{pdf_path}' not found!")
        print("💡 Make sure sample_job.pdf is in the same folder!")
        return None
    except Exception as e:
        print(f"\n❌ ERROR reading PDF: {e}")
        return None

def extract_job_details(text):
    """Use AI to extract structured job information"""
    
    if not text:
        return None
    
    print("\n🤖 Sending data to Gemini AI for extraction...")
    print("⏳ This will take 5-10 seconds...\n")
    
    prompt = f"""You are an expert at extracting information from Indian government job notifications.

Extract these details and return ONLY valid JSON (no extra text):

{{
    "organization_name": "name of hiring organization",
    "post_name": "job title/designation",
    "total_vacancies": "number of positions",
    "salary": "salary range or pay scale",
    "location": "job location/posting place",
    "qualifications": "educational qualifications required",
    "experience_required": "work experience needed",
    "application_deadline": "last date to apply",
    "application_fee": "fee amount if mentioned",
    "age_limit": "age criteria if mentioned"
}}

If information not found, use "Not mentioned".
Return ONLY the JSON object.

Government Job Notification Text:
{text[:8000]}
"""
    
    try:
        response = client.chat.completions.create(
            model="gemini-2.5-flash",
            messages=[
                {"role": "system", "content": "You extract data and return only valid JSON."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.1
        )
        
        result = response.choices[0].message.content
        print("✅ AI extraction completed successfully!")
        return result
    
    except Exception as e:
        print(f"\n❌ ERROR with AI: {e}")
        print("\n💡 Check if your API key is correct!")
        return None

# MAIN PROGRAM STARTS HERE
if __name__ == "__main__":
    
    print("\n" + "=" * 60)
    print("           STARTING EXTRACTION PROCESS")
    print("=" * 60)
    
    # File name
    pdf_file = "sample_job.pdf"
    
    # Step 1: Extract text from PDF
    print("\n📍 STEP 1: Reading PDF file...")
    pdf_text = extract_pdf_text(pdf_file)
    
    if pdf_text:
        # Step 2: Use AI to extract data
        print("\n📍 STEP 2: Extracting structured data with AI...")
        job_data = extract_job_details(pdf_text)
        
        if job_data:
            # Display results
            print("\n" + "=" * 60)
            print("           📊 EXTRACTED JOB DATA")
            print("=" * 60)
            print(job_data)
            print("=" * 60)
            
            # Save to file
            output_file = "extracted_job_data.json"
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(job_data)
            
            print(f"\n💾 Saved to file: {output_file}")
            print("\n" + "=" * 60)
            print("       ✅ EXTRACTION COMPLETED SUCCESSFULLY!")
            print("=" * 60)
        else:
            print("\n❌ Failed to extract data")
    else:
        print("\n❌ Failed to read PDF")
    
    print("\n👋 Thanks for using JobYaari PDF Extractor!")
    print("\n")
    input("Press ENTER to exit...")
