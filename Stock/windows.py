import tkinter as tk
import reptile
def create_window():
    # 創建主視窗
    root = tk.Tk()

    # 設定視窗標題
    root.title("在視窗中新增輸入欄位")

    # 設定視窗大小
    root.geometry("300x200")

    # 創建一個輸入欄位
    stock_code_entry = tk.Entry(root)
    stock_code_entry.pack(side="top", padx=10, pady=10)  # 使用 pack() 方法並指定 side 屬性來使其保持在最上方

    # 創建一個按鈕，點擊後更新文字
    button = tk.Button(root, text="查詢", command=lambda: update_text(stock_code_entry, result_label))
    button.pack(padx=10, pady=5)

    # 創建一個標籤，用於顯示股票資訊
    result_label = tk.Label(root, text="")
    result_label.pack(padx=10, pady=10)

    # 顯示視窗
    root.mainloop()
   

def update_text(stock_code_entry, result_label):
    stock_code = stock_code_entry.get()
    tree = reptile.getUrl(stock_code)
    text = reptile.getName(tree) + '股價：'+ str(reptile.getPrice(tree))+' '
    text1 = '漲跌:'+ str(reptile.getUpDown(tree)) + ' '
    text2 = '漲跌幅:' + str(reptile.getPercentage(tree))
    result_label.config(text=text + text1 + text2)

create_window()