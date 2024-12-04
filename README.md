# qr_codes
Personal Qr Codes

Adjusted this gist: https://www.geeksforgeeks.org/how-to-generate-qr-codes-with-a-custom-logo-using-python/ to a cli.

Install deps:
```bash 
pip install click Pillow qrcode[pil]
```

Run:
```bash
python3 generate.py --logo-path logos/LinkedIn/LI-In-Bug.png --url "https://www.linkedin.com/in/yale-hartmann/" --qr-color "#0a66c3" --output codes/linkedin.png
```