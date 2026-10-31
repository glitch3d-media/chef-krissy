from pathlib import Path
from reportlab.lib.pagesizes import A4, LEGAL, LETTER
from reportlab.lib.units import inch
from reportlab.pdfgen.canvas import Canvas


def export_menu_pdf(
    data: dict,
    output_path: str,
    page_size: str = "Letter",
    orientation: str = "portrait",
) -> str:
    page_sizes = {"Letter": LETTER, "A4": A4, "Legal": LEGAL}
    
    # Handle page size and orientation
    if orientation == "landscape":
        page_sizes = {k: v[::-1] for k, v in page_sizes.items()}
    
    canvas = Canvas(output_path, pagesize=page_sizes[page_size])
    width, height = page_sizes[page_size]

    # Start the text object
    textobject = canvas.beginText()
    textobject.setFont("Helvetica-Bold", 18)
    textobject.setTextOrigin(inch, height - 1 * inch)
    
    # Header info (using the correct meta schema)
    meta = data.get("meta", {})
    textobject.textOut("MENU")
    textobject.moveCursor(0, -25)
    textobject.setFont("Helvetica", 12)
    textobject.textOut(f"Business Name: {meta.get('business_name', '')}")
    textobject.moveCursor(0, -20)
    textobject.textOut(f"Contact Info: {meta.get('contact_info', '')}")
    textobject.moveCursor(0, -30)

    # Iterate through schedule
    schedule = data.get("schedule", {})
    for day, meals in schedule.items():
        textobject.setFont("Helvetica-Bold", 14)
        textobject.textOut(f"{day}:")
        textobject.moveCursor(0, -20)
        
        # Breakfast items (list of dicts)
        textobject.setFont("Helvetica", 12)
        textobject.textOut("  Breakfast:")
        textobject.moveCursor(0, -15)
        for item in meals.get("breakfast", []):
            name = item.get("name", "")
            price = item.get("price", "")
            textobject.textOut(f"    - {name} ({price})")
            textobject.moveCursor(0, -15)
        
        # Lunch items (list of dicts)
        textobject.setFont("Helvetica", 12)
        textobject.textOut("  Lunch:")
        textobject.moveCursor(0, -15)
        for item in meals.get("lunch", []):
            name = item.get("name", "")
            price = item.get("price", "")
            textobject.textOut(f"    - {name} ({price})")
            textobject.moveCursor(0, -15)
        
        textobject.moveCursor(0, -10) # Extra space between days

    # Draw the text object to the canvas and save
    canvas.drawText(textobject)
    canvas.save()

    return str(Path(output_path).resolve())
