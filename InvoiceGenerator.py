from tkinter import *
import tkinter.ttk as ttk
import tkinter.messagebox as tkMessageBox
import time
from reportlab.pdfgen import canvas
import webbrowser, os

try:
    os.mkdir("C:\\InvoiceGenerator")
except FileExistsError:
    pass

class Header:
    def __init__(self, CustomerName, CustomerContact):
        self.InvoiceNumber = time.time()
        self.CustomerName = CustomerName
        self.CustomerContact = CustomerContact
        timedate = time.asctime()
        self.date = timedate[4:8] + timedate[8:10] + ", " + timedate[20:24] + "."
        self.time = " " + timedate[11:20]

class Product:
    def __init__(self, name, quantity, rate, tax, discount):
        self.name = name
        self.quantity = quantity
        self.rate = rate
        self.tax = tax
        self.total = (quantity * rate) - discount
        self.discount = discount

root = Tk()
root.title("E-INVOICE GENERATOR")
width, height = 700, 400
screen_width, screen_height = root.winfo_screenwidth(), root.winfo_screenheight()
x, y = (screen_width / 2) - (width / 2), (screen_height / 2) - (height / 2)
root.geometry(f"{width}x{height}+{int(x)}+{int(y)}")
root.resizable(0, 0)
root.config(bg="#6666ff")

PRODUCTNAME = StringVar()
QUANTITY = IntVar(value=1)
RATE = IntVar(value=0)
TAX = IntVar(value=0)
DISCOUNT = IntVar(value=0)
CustomerName = StringVar()
CustomerContact = StringVar()

Products = []

def print_invoice():
    head = Header(CustomerName.get(), CustomerContact.get())
    pdf_path = f"C:\\InvoiceGenerator\\{int(head.InvoiceNumber)}.pdf"
    pdf = canvas.Canvas(pdf_path)
    
    y_coordinate = 650
    x = 1

    for item in Products:
        curr_product = Product(item[0], item[1], item[2], item[5], item[3])
        pdf.drawString(35, y_coordinate, str(x))
        x += 1
        pdf.setFont("Courier-Bold", 9)
        y_coordinate -= 20

    pdf.setFont("Courier-Bold", 11)
    pdf.save()
    webbrowser.open(pdf_path)

def submit_data():
    product = PRODUCTNAME.get()
    quantity = QUANTITY.get()
    rate = RATE.get()

    discount = float((quantity * rate) * (DISCOUNT.get() / 100))
    total = float(quantity * rate - discount)
    tax = float(TAX.get() * 0.01 * total)

    Products.append((product, quantity, rate, discount, total, tax))
    tree.delete(*tree.get_children())
    
    for data in Products:
        tree.insert('', 'end', values=data)

    PRODUCTNAME.set("")
    QUANTITY.set(1)
    RATE.set(0)
    TAX.set(0)
    DISCOUNT.set(0)

def delete_data():
    if not tree.selection():
        tkMessageBox.showwarning('', 'Please select an item first!', icon="warning")
    else:
        result = tkMessageBox.askquestion('', 'Are you sure you want to delete this item?', icon="warning")
        if result == 'yes':
            cur_item = tree.focus()
            contents = tree.item(cur_item)
            selected_item = contents['values']
            tree.delete(cur_item)
            
            for i, item in enumerate(Products):
                if item[0] == selected_item[0]:
                    del Products[i]
                    break

def add_new_window():
    global NewWindow
    PRODUCTNAME.set("")
    QUANTITY.set(1)
    RATE.set(0)

    NewWindow = Toplevel()
    NewWindow.title("Add New Item")
    NewWindow.geometry("400x330+100+100")
    NewWindow.resizable(0, 0)

    # Frame setup
    FormTitle = Frame(NewWindow)
    FormTitle.pack(side=TOP)
    Form = Frame(NewWindow)
    Form.pack(side=TOP, pady=10)

    # Labels
    Label(FormTitle, text="Add Item", font=('arial', 16), bg="#66ff66", width=300).pack(fill=X)
    labels = ["Product Name", "Quantity", "Rate", "Tax (%)", "Discount (%)", "Customer Name", "Customer Contact"]
    for i, label in enumerate(labels):
        Label(Form, text=label, font=('arial', 14), bd=5).grid(row=i, sticky=W)

    # Entry fields
    entries = [
        Entry(Form, textvariable=PRODUCTNAME, font=('arial', 14)),
        Entry(Form, textvariable=QUANTITY, font=('arial', 14)),
        Entry(Form, textvariable=RATE, font=('arial', 14)),
        Entry(Form, textvariable=TAX, font=('arial', 14)),
        Entry(Form, textvariable=DISCOUNT, font=('arial', 14)),
        Entry(Form, textvariable=CustomerName, font=('arial', 14)),
        Entry(Form, textvariable=CustomerContact, font=('arial', 14))
    ]

    for i, entry in enumerate(entries):
        entry.grid(row=i, column=1)

    Button(Form, text="Add Item to Cart", width=50, command=submit_data).grid(row=7, columnspan=2, pady=10)

# Frames setup
Top = Frame(root, width=500, bd=1, relief=SOLID)
Top.pack(side=TOP)
Mid = Frame(root, width=500, bg="#6666ff")
Mid.pack(side=TOP)
MidLeft = Frame(Mid, width=100)
MidLeft.pack(side=LEFT, pady=10)
MidRight = Frame(Mid, width=100)
MidRight.pack(side=RIGHT, pady=10)
TableMargin = Frame(root, width=500)
TableMargin.pack(side=TOP)

# Labels
Label(Top, text="Shop Name", font=('arial', 16), width=500).pack(fill=X)

# Buttons
Button(MidLeft, text="Add New Item", bg="#66ff66", command=add_new_window).pack()
Button(MidRight, text="Remove Selected Item", bg="red", command=delete_data).pack(side=RIGHT)
Button(TableMargin, text="Print Invoice", bg="lightgreen", command=print_invoice).pack(side=BOTTOM)

# Table
scrollbarx = Scrollbar(TableMargin, orient=HORIZONTAL)
scrollbary = Scrollbar(TableMargin, orient=VERTICAL)
tree = ttk.Treeview(TableMargin, columns=("Product Name", "Quantity", "Rate", "Discount", "Total", "Tax"),
                    height=400, selectmode="extended", yscrollcommand=scrollbary.set, xscrollcommand=scrollbarx.set)

scrollbary.config(command=tree.yview)
scrollbary.pack(side=RIGHT, fill=Y)
scrollbarx.config(command=tree.xview)
scrollbarx.pack(side=BOTTOM, fill=X)

# Table headers
for col in ["Product Name", "Quantity", "Rate", "Discount", "Total", "Tax"]:
    tree.heading(col, text=col, anchor=W)

tree.column('#0', width=0)
tree.pack()
root.mainloop()
