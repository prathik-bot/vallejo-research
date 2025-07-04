git clone git@github.com:prathik-bot/vallejo-research.git
cd vallejo-research

python3 -m venv venv
source venv/bin/activate      # On Windows: venv\Scripts\activate
pip install -r requirements.txt

PURPLEAIR_API_KEY=your_api_key_here

python run.py

Real sensor data: http://localhost:5001/api/sensors

Mock sensor data: http://localhost:5001/api/mock-sensors

