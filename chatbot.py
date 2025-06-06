import os
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import google.generativeai as genai
from google.generativeai.types import GenerationConfig
from googletrans import Translator
from gtts import gTTS
import base64
import io
import logging
import re
import random
from datetime import datetime, timedelta
from PIL import Image
import tempfile

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)
CORS(app)

GEMINI_API_KEY = ""  # REPLACE WITH YOUR GEMINI API KEY

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel(model_name="gemini-2.0-flash") 

translator = Translator()

SYSTEM_INSTRUCTIONS_EN = """
You are a helpful and knowledgeable Government Services Assistant for India.
Your role is to provide accurate, easy-to-understand information about government services in simple language.

You can help with:
- Tax explanations and procedures (Income Tax, GST, Property Tax, etc.)
- Government schemes and benefits (PM-KISAN, Ayushman Bharat, etc.)
- Digital services (Aadhaar, PAN, Passport, Driving License)
- Ration card and PDS information
- Pension schemes and status
- Banking and financial services
- Public grievances and complaints
- Municipal services and civic issues
- Educational schemes and scholarships
- Healthcare services and schemes
- Employment programs (MGNREGA, etc.)

When users ask about ration card or pension status, provide realistic sample information.
For pothole complaints with images, acknowledge the report and ask for location details.

Always be respectful, helpful, and supportive. Explain complex procedures in simple steps.

Note:
- Do not use emojis in your responses
- Do not use bold text in your responses
- When possible, give your response in clean bullet points to keep it neat
- Use simple language that everyone can understand
- Provide step-by-step guidance for government procedures
- give in a neat format which is readable
"""

SYSTEM_INSTRUCTIONS_TE = """
మీరు భారతదేశ ప్రభుత్వ సేవల కోసం సహాయకారిగా పనిచేస్తున్నారు.
మీ పాత్ర ప్రభుత్వ సేవల గురించి సరళమైన భాషలో ఖచ్చితమైన, సులభంగా అర్థమయ్యే సమాచారాన్ని అందించడం.

మీరు ఈ విషయాల్లో సహాయం చేయగలరు:
- పన్ను వివరణలు మరియు విధానాలు (ఆదాయపు పన్ను, జిఎస్టి, ఆస్తి పన్ను మొదలైనవి)
- ప్రభుత్వ పథకాలు మరియు ప్రయోజనాలు (పిఎం-కిసాన్, ఆయుష్మాన్ భారత్ మొదలైనవి)
- డిజిటల్ సేవలు (ఆధార్, పాన్, పాస్‌పోర్ట్, డ్రైవింగ్ లైసెన్స్)
- రేషన్ కార్డ్ మరియు పిడిఎస్ సమాచారం
- పెన్షన్ పథకాలు మరియు స్థితి
- బ్యాంకింగ్ మరియు ఆర్థిక సేవలు
- ప్రజా ఫిర్యాదులు మరియు ఫిర్యాదులు
- మునిసిపల్ సేవలు మరియు పౌర సమస్యలు

రేషన్ కార్డ్ లేదా పెన్షన్ స్థితి గురించి అడిగినప్పుడు వాస్తవిక నమూనా సమాచారాన్ని అందించండి.
గొయ్యి ఫిర్యాదుల కోసం చిత్రాలతో, నివేదికను అంగీకరించండి మరియు స్థాన వివరాలను అడగండి.

ఎల్లప్పుడూ గౌరవంగా, సహాయకంగా మరియు మద్దతుగా ఉండండి.

గమనిక:
- స్పందనలో ఎమోజీలు ఉపయోగించవద్దు
- బోల్డ్ టెక్స్ట్ ఉపయోగించవద్దు
- సాధ్యమైనప్పుడు సమాధానాలను పాయింట్ల రూపంలో చక్కగా ఇవ్వండి
- అందరికీ అర్థమయ్యే సరళమైన భాషను ఉపయోగించండి
"""

def generate_fake_ration_card_info():
    card_numbers = ["AP12345678901234", "TG98765432109876", "KA56789012345678", "TN34567890123456"]
    statuses = ["Active", "Active", "Pending Renewal", "Active"]
    card_types = ["APL", "BPL", "AAY", "APL"]
    card_info = {
        "card_number": random.choice(card_numbers),
        "status": random.choice(statuses),
        "card_type": random.choice(card_types),
        "head_of_family": random.choice(["Rajesh Kumar", "Priya Sharma", "Suresh Reddy", "Lakshmi Devi"]),
        "family_members": random.randint(3, 6),
        "last_transaction": (datetime.now() - timedelta(days=random.randint(1, 30))).strftime("%d-%m-%Y"),
        "monthly_quota": f"{random.randint(15, 35)} kg rice, {random.randint(5, 10)} kg wheat",
        "fair_price_shop": f"Shop No. {random.randint(1, 50)}, {random.choice(['Gandhi Nagar', 'Nehru Colony', 'Ambedkar Street', 'Indira Nagar'])}"
    }
    return card_info

def generate_fake_pension_info():
    pension_types = ["Old Age Pension", "Widow Pension", "Disability Pension", "Ex-Serviceman Pension"]
    statuses = ["Active", "Active", "Under Verification", "Active"]
    pension_info = {
        "pension_type": random.choice(pension_types),
        "status": random.choice(statuses),
        "beneficiary_name": random.choice(["Ramesh Chandra", "Kamala Devi", "Subhash Rao", "Meera Singh"]),
        "monthly_amount": f"Rs. {random.randint(1000, 3000)}",
        "last_payment": (datetime.now() - timedelta(days=random.randint(1, 45))).strftime("%d-%m-%Y"),
        "bank_account": f"{random.randint(1000, 9999)}",
        "next_payment": (datetime.now() + timedelta(days=random.randint(1, 30))).strftime("%d-%m-%Y"),
        "pension_id": f"PEN{random.randint(100000, 999999)}"
    }
    return pension_info

def translate_text(text, target_language, source_language='auto'):
    if text:
        try:
            translation = translator.translate(text, dest=target_language, src=source_language)
            return translation.text
        except Exception as e:
            logging.error(f"Translation error ({source_language} to {target_language}): {e}")
            return text
    return ""

def synthesize_speech(text, language_code):
    if text and language_code in ['en', 'te']:
        try:
            cleaned_text = text.replace('*', '') 
            tts = gTTS(text=cleaned_text, lang=language_code)
            audio_segment = io.BytesIO()
            tts.write_to_fp(audio_segment)
            audio_segment.seek(0)
            audio_bytes = audio_segment.read()
            return base64.b64encode(audio_bytes).decode('utf-8')
        except Exception as e:
            logging.error(f"TTS error ({language_code}): {e}")
            return None
    return None

@app.route("/chatbot")
def chatbot_page():
    return render_template("chatbot.html")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    try:
        user_input = request.form.get("user_input", "")
        audio_data = request.form.get("audio_data")
        image_data = request.form.get("image_data")
        target_language = request.form.get("target_language", "en")
        user_language = request.form.get("user_language", "en")

        logging.info(f"Received request - Input: {user_input[:50]}..., Image: {'Yes' if image_data else 'No'}")

        if audio_data:
            logging.info(f"Received audio data in {user_language} - processing not implemented on backend")
            user_input = translate_text("Processing audio input...", 'en', user_language)

        # Handle image upload (pothole reporting)
        if image_data:
            pothole_keywords = ['pothole', 'road', 'street', 'damage', 'repair', 'infrastructure']
            is_pothole_complaint = any(keyword in user_input.lower() for keyword in pothole_keywords) if user_input else False

            if not is_pothole_complaint:
                error_response = "Please specify that this is a pothole or road-related complaint when uploading an image. For example: 'I want to report a pothole' along with your image."
                translated_error = translate_text(error_response, target_language, 'en')
                audio_output = synthesize_speech(translated_error, target_language)
                return jsonify({"response": translated_error, "audio": audio_output})

            # If image is valid (no AI check), register complaint
            complaint_ref = f"RD{random.randint(100000, 999999)}"
            response_text = f"""Thank you for reporting this road issue! 

Your pothole complaint has been successfully registered and forwarded to higher officials:

• Complaint Reference: {complaint_ref}
• Status: Registered and Escalated
• Department: Municipal Corporation - Roads Division
• Priority: High (Image Evidence Provided)
• Expected Response: 2-3 working days
• SMS Confirmation: Will be sent within 24 hours

The concerned authorities have been notified and will inspect the location based on the image evidence provided. Thank you for helping improve our city's infrastructure!

You can track your complaint status using the reference number: {complaint_ref}"""
            translated_response = translate_text(response_text, target_language, 'en')
            audio_output = synthesize_speech(translated_response, target_language)
            logging.info("Image processed successfully, complaint registered automatically")
            return jsonify({"response": translated_response, "audio": audio_output})

        if not user_input.strip():
            error_msg = translate_text("Please enter your message or provide audio input.", target_language, 'en')
            return jsonify({"response": error_msg})

        translated_user_input_en = translate_text(user_input, 'en', user_language)
        user_input_lower = translated_user_input_en.lower()
        
        # Ration card query
        if any(word in user_input_lower for word in ['ration card', 'ration', 'pds', 'food card']):
            ration_info = generate_fake_ration_card_info()
            response_text = f"""Here is your ration card information:

• Card Number: {ration_info['card_number']}
• Status: {ration_info['status']}
• Card Type: {ration_info['card_type']}
• Head of Family: {ration_info['head_of_family']}
• Family Members: {ration_info['family_members']}
• Monthly Quota: {ration_info['monthly_quota']}
• Last Transaction: {ration_info['last_transaction']}
• Fair Price Shop: {ration_info['fair_price_shop']}

If you need to update any information or have issues with your ration card, please visit your nearest Common Service Center or contact the Food & Civil Supplies Department."""

        # Pension query
        elif any(word in user_input_lower for word in ['pension', 'pension status', 'pension scheme']):
            pension_info = generate_fake_pension_info()
            response_text = f"""Here is your pension information:

• Pension Type: {pension_info['pension_type']}
• Status: {pension_info['status']}
• Beneficiary: {pension_info['beneficiary_name']}
• Monthly Amount: {pension_info['monthly_amount']}
• Last Payment: {pension_info['last_payment']}
• Next Payment: {pension_info['next_payment']}
• Bank Account: {pension_info['bank_account']}
• Pension ID: {pension_info['pension_id']}

For any pension-related queries, contact the Social Welfare Department or visit your nearest Common Service Center."""

        # Pothole location query (text only)
        elif any(word in user_input_lower for word in ['pothole', 'road', 'location', 'area', 'street', 'complaint']):
            complaint_ref = f"RD{random.randint(100000, 999999)}"
            response_text = f"""Thank you for providing the location details! 

Your pothole complaint has been successfully registered:

• Complaint Reference: {complaint_ref}
• Status: Registered
• Department: Municipal Corporation - Roads Division
• Expected Response: 3-5 working days
• SMS Confirmation: Will be sent within 24 hours

The concerned authorities will inspect the reported location and take necessary action. You can track your complaint status using the reference number.

Thank you for helping improve our city's infrastructure!"""

        else:
            # General government services query
            system_instructions = SYSTEM_INSTRUCTIONS_EN if target_language == 'en' else SYSTEM_INSTRUCTIONS_TE
            chat = model.start_chat(history=[])
            response = chat.send_message(f"{system_instructions}\n\nUser question (in English): {translated_user_input_en}")
            response_text = response.text if response.text else translate_text("Sorry, I didn't get a response.", target_language, 'en')

        # Clean response
        response_text = response_text.replace('*', '')

        # Translate response
        translated_response = translate_text(response_text, target_language, 'en')
        translated_response = translated_response.replace('*', '')

        # Generate audio
        audio_output = synthesize_speech(translated_response, target_language)
        
        logging.info("Request processed successfully")
        return jsonify({"response": translated_response, "audio": audio_output})

    except Exception as e:
        logging.error(f"Chat API error: {str(e)}", exc_info=True)
        error_message = translate_text("Sorry, there was a technical issue. Please try again.", target_language, 'en')
        return jsonify({"response": error_message}), 500

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')