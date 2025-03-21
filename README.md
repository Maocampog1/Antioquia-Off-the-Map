# Antioquia-Off-the-Map

## 🚀 Running Instructions

Follow these steps to set up and run the project locally.

### Requirements
- Python
- A Google Maps API Key

**1. Clone the repository**

```
git clone https://github.com/Maocampog1/Antioquia-Off-the-Map.git
cd Antiquia-Off-The-Map
```

**2. Set up a virtual environment**

Create and activate a virtual environment

- **Windows:**

```
python -m venv env
env\Scripts\activate
```

- **Mac/Linux:**

```
python -m venv venv
source venv/bin/activate
```

**3. Install dependencies**

```
pip install -r requirements.txt
cd theme/static_src/
npm install
cd ../..
```

**4. Create a .env file to store the private KEYS**
```
echo "GOOGLE_MAPS_API_KEY=YOUR_API_KEY" > .env
```
✅ Ensuring the .env File is in UTF-8 Encoding
To avoid errors, you must ensure that the .env file is encoded in UTF-8. If it is not, follow these steps:

1️⃣ Open VS Code and open the .env file.
2️⃣ Check the encoding:

Look at the bottom right corner of the VS Code window.
If it says UTF-16 or anything other than UTF-8, click on it.
3️⃣ A menu will appear at the top center of the screen. Click "Save with Encoding".
4️⃣ In the list of encodings, select "UTF-8" and save the file.
Now your .env file is properly formatted and ready to use! 🚀

Each Google Maps Web Service request requires an API key. API keys
are generated in the 'Credentials' page of the 'APIs & Services' tab of [Google Cloud console](https://console.cloud.google.com/apis/credentials).

Once you generated your key, change it in the .env file

**5. Run the development server**

```
python manage.py runserver
```

The app will be available at http://127.0.0.1:8000/.
