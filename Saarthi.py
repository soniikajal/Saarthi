from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import random

app = Flask(__name__)


emotions_shlokas = {
    "1": {  # Anxiety/Worry
        "shlokas": [
            {
                "shlok": "कर्मण्येवाधिकारस्ते मा फलेषु कदाचन। मा कर्मफलहेतुर्भूर्मा ते सङ्गोऽस्त्वकर्मणि॥",
                "chapter": "2.47",
                "hindi_meaning": "आपका कर्म करने में ही अधिकार है, फल में कभी नहीं। इसलिए कर्म के फल के हेतु मत बनो, और अकर्म (कर्म न करने) में भी आपकी आसक्ति न हो।",
                "english_meaning": "You have a right to perform your prescribed duties, but you are not entitled to the fruits of your actions. Never consider yourself to be the cause of the results, and never be attached to not doing your duty."
            }
        ]
    },
    "2": {  # Sadness
        "shlokas": [
            {
                "shlok": "वासांसि जीर्णानि यथा विहाय नवानि गृह्णाति नरोऽपराणि। तथा शरीराणि विहाय जीर्णान्यन्यानि संयाति नवानि देही॥",
                "chapter": "2.22",
                "hindi_meaning": "जैसे मनुष्य पुराने वस्त्रों को त्याग कर नए वस्त्र धारण करता है, वैसे ही आत्मा पुराने शरीरों को त्याग कर नए शरीर धारण करता है।",
                "english_meaning": "As a person puts on new garments, giving up old ones, similarly, the soul accepts new material bodies, giving up the old and useless ones."
            }
        ]
    },
    "3": {  # Anger
        "shlokas": [
            {
                "shlok": "क्रोधाद्भवति संमोहः संमोहात्स्मृतिविभ्रमः। स्मृतिभ्रंशाद्बुद्धिनाशो बुद्धिनाशात्प्रणश्यति॥",
                "chapter": "2.63",
                "hindi_meaning": "क्रोध से मनुष्य में मोह उत्पन्न होता है, मोह से स्मृति भ्रमित हो जाती है, स्मृति भ्रमित होने से बुद्धि का नाश होता है, और बुद्धि नष्ट होने से मनुष्य का पतन हो जाता है।",
                "english_meaning": "From anger, delusion arises, and from delusion bewilderment of memory. When memory is bewildered, intelligence is lost, and when intelligence is lost, one falls down again into the material pool."
            }
        ]
    },
    "4": {  # Confusion
        "shlokas": [
            {
                "shlok": "यदा यदा हि धर्मस्य ग्लानिर्भवति भारत। अभ्युत्थानमधर्मस्य तदात्मानं सृजाम्यहम्॥",
                "chapter": "4.7",
                "hindi_meaning": "हे भारत, जब-जब धर्म की हानि और अधर्म की वृद्धि होती है, तब-तब मैं स्वयं को प्रकट करता हूँ।",
                "english_meaning": "Whenever and wherever there is a decline in righteousness and an increase in unrighteousness, at that time I manifest myself."
            }
        ]
    },
    "5": {  # Fear
        "shlokas": [
            {
                "shlok": "अभयं सत्त्वसंशुद्धिर्ज्ञानयोगव्यवस्थितिः। दानं दमश्च यज्ञश्च स्वाध्यायस्तप आर्जवम्॥",
                "chapter": "16.1",
                "hindi_meaning": "अभय, अंतःकरण की शुद्धि, ज्ञान और योग में स्थिरता, दान, इन्द्रिय संयम, यज्ञ, स्वाध्याय, तप और सरलता - ये दैवी संपदा के लक्षण हैं।",
                "english_meaning": "Fearlessness, purity of heart, steadfastness in knowledge and yoga, charity, self-control, sacrifice, study of the scriptures, austerity, and simplicity are the divine qualities."
            }
        ]
    },
    "6": {  # Happiness
        "shlokas": [
            {
                "shlok": "सुखदुःखे समे कृत्वा लाभालाभौ जयाजयौ। ततो युद्धाय युज्यस्व नैवं पापमवाप्स्यसि॥",
                "chapter": "2.38",
                "hindi_meaning": "सुख और दुःख, लाभ और हानि, जीत और हार - इन सबको समान समझकर युद्ध के लिए तैयार हो जाओ। इस प्रकार तुम पाप से नहीं बंधोगे।",
                "english_meaning": "Fight for the sake of duty, treating alike happiness and distress, loss and gain, victory and defeat. Fulfilling your responsibility in this way, you will never incur sin."
            }
        ]
    },
    "7": {  # Gratitude
        "shlokas": [
            {
                "shlok": "यत्करोषि यदश्नासि यज्जुहोषि ददासि यत्। यत्तपस्यसि कौन्तेय तत्कुरुष्व मदर्पणम्॥",
                "chapter": "9.27",
                "hindi_meaning": "हे कुंतीपुत्र, तुम जो कुछ भी करते हो, जो खाते हो, जो हवन करते हो, जो दान देते हो, जो तप करते हो, वह सब मुझे अर्पित करो।",
                "english_meaning": "Whatever you do, whatever you eat, whatever you offer or give away, and whatever austerities you perform – do that, O son of Kunti, as an offering to Me."
            }
        ]
    },
    "8": {  # Hope
        "shlokas": [
            {
                "shlok": "श्रद्धावाँल्लभते ज्ञानं तत्परः संयतेन्द्रियः। ज्ञानं लब्ध्वा परां शान्तिमचिरेणाधिगच्छति॥",
                "chapter": "4.39",
                "hindi_meaning": "श्रद्धावान, तत्पर और संयमित इंद्रियों वाला व्यक्ति ज्ञान प्राप्त करता है और ज्ञान प्राप्त करके वह शीघ्र ही परम शांति को प्राप्त होता है।",
                "english_meaning": "One who has faith, who is dedicated and who has controlled the senses, attains knowledge. Having attained knowledge, one quickly attains supreme peace."
            }
        ]
    },
}

# Initial user state tracking
user_sessions = {}

@app.route("/saarthi", methods=['POST'])
def bot():
    # Get incoming message details
    incoming_msg = request.values.get('Body', '').strip().lower()
    sender_id = request.values.get('From', '')

    # Create response object
    resp = MessagingResponse()

    # New user or reset
    if incoming_msg in ["hi", "hello", "namaste"] or sender_id not in user_sessions:
        user_sessions[sender_id] = {"state": "initial"}
        response_text = (
            "🙏 *Welcome to SAARTHI* 🙏\n\n"
            "I can share a shlok from Bhagavad Gita based on your current emotion.\n\n"
            "Please select one of the following emotions by typing the number:\n\n"
            "1. Anxiety/Worry\n"
            "2. Sadness\n"
            "3. Anger\n"
            "4. Confusion\n"
            "5. Fear\n"
            "6. Happiness\n"
            "7. Gratitude\n"
            "8. Hope\n\n"
            "Type *reset* anytime to start over."
        )
        resp.message(response_text)
        return str(resp)

    # Reset command
    if incoming_msg == "reset":
        user_sessions[sender_id] = {"state": "initial"}
        response_text = (
            "🙏 *Welcome back to SAARTHI* 🙏\n\n"
            "Please select one of the following emotions by typing the number:\n\n"
            "1. Anxiety/Worry\n"
            "2. Sadness\n"
            "3. Anger\n"
            "4. Confusion\n"
            "5. Fear\n"
            "6. Happiness\n"
            "7. Gratitude\n"
            "8. Hope"
        )
        resp.message(response_text)
        return str(resp)

    # Process emotion selection
    if incoming_msg in emotions_shlokas.keys():
        emotion = incoming_msg
        shlokas_list = emotions_shlokas[emotion]["shlokas"]
        selected_shloka = random.choice(shlokas_list)
        response_text = (
            f"*Bhagavad Gita Chapter {selected_shloka['chapter']}*\n\n"
            f"*Sanskrit Shloka:*\n{selected_shloka['shlok']}\n\n"
            f"*Hindi Meaning:*\n{selected_shloka['hindi_meaning']}\n\n"
            f"*English Meaning:*\n{selected_shloka['english_meaning']}\n\n"
            f"Type any emotion number to receive another shloka or *reset* to start over."
        )
        user_sessions[sender_id] = {"state": "received_shloka", "emotion": emotion}
        resp.message(response_text)
        return str(resp)
    else:
        resp.message("I didn't understand your response. Please select a number from 1-8 for emotions or type *reset*.")
        return str(resp)

if __name__ == "__main__":
    app.run(debug=True, port=5001)
