# Antioquia-Off-the-Map

## 🚀 Running Instructions

Follow these steps to set up and run the project locally.

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
```

**4. Run the development server**

```
python manage.py tailwind start
```

**Open a new terminal**
```
python manage.py runserver
```

The app will be available at http://127.0.0.1:8000/.
