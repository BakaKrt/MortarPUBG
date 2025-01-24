import tkinter as tk

def handle_ctrl_left_click(event):
    if event.state & 0x0004:  # Проверяем, зажат ли Ctrl (0x0004 - маска для Ctrl)
        print("Ctrl + Левый клик!")
        # Здесь ваш код для обработки события

def main():
    root = tk.Tk()
    root.geometry("300x200")

    canvas = tk.Canvas(root, bg="white")
    canvas.pack(expand=True, fill="both")

    canvas.bind("<Button-1>", handle_ctrl_left_click) # Обрабатываем левый клик

    root.mainloop()

if __name__ == "__main__":
    main()

