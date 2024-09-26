import tkinter as tk
import screeninfo
import time

WORK_DURATION = 25*60  # 25分間の作業タイマー (秒数指定)
BREAK_DURATION = 5*60   # 5分間の休憩タイマー (秒数指定)

def create_blackout_window(screen):
    blackout_root = tk.Tk()
    geometry_string = f"{screen.width}x{screen.height}+{screen.x}+{screen.y}"
    blackout_root.geometry(geometry_string)
    blackout_root.overrideredirect(1)  # ウィンドウ枠を非表示に
    blackout_root.configure(background='black')
    blackout_root.lift()
    blackout_root.attributes('-topmost', True)
    return blackout_root

def create_small_timer_window(screen, duration_seconds):
    timer_root = tk.Tk()
    small_window_width = 200
    small_window_height = 100
    x_position = screen.x + 10  # ディスプレイの左上に表示
    y_position = screen.y + 10
    geometry_string = f"{small_window_width}x{small_window_height}+{x_position}+{y_position}"
    timer_root.geometry(geometry_string)
    timer_root.attributes('-topmost', True)  # 常に最前面に表示

    timer_label = tk.Label(timer_root, text="", fg="black", bg="white", font=("Helvetica", 24))
    timer_label.pack(expand=True)

    def countdown(count):
        if count > 0:
            mins, secs = divmod(count, 60)
            time_format = '{:02d}:{:02d}'.format(mins, secs)
            timer_label.config(text=time_format)
            timer_root.after(1000, countdown, count-1)
        else:
            timer_root.destroy()
            show_blackout_on_all_screens()

    countdown(duration_seconds)
    return timer_root

def show_blackout_on_all_screens():
    screens = screeninfo.get_monitors()
    roots = []

    for screen in screens:
        root = create_blackout_window(screen)
        roots.append(root)

    # メインスクリーンのウィンドウに休憩メッセージとボタンを配置
    main_screen_root = roots[1]  # メインディスプレイのウィンドウ
    
    label = tk.Label(main_screen_root, text="休憩時間です！", fg="white", bg="black", font=("Helvetica", 48))
    label.pack(expand=True)

    timer_label = tk.Label(main_screen_root, text=f"{BREAK_DURATION // 60:02d}:00", fg="white", bg="black", font=("Helvetica", 48))
    timer_label.pack()

    start_break_timer(BREAK_DURATION, timer_label, roots)

    main_screen_root.mainloop()

def start_work_timer():
    screens = screeninfo.get_monitors()
    if len(screens) > 2:  # 3番目のスクリーンがある場合
        small_timer_window = create_small_timer_window(screens[2], WORK_DURATION)
        small_timer_window.mainloop()
    else:
        time.sleep(WORK_DURATION)
        show_blackout_on_all_screens()

def start_break_timer(duration_seconds, timer_label, roots):
    def countdown(count):
        if count > 0:
            mins, secs = divmod(count, 60)
            time_format = '{:02d}:{:02d}'.format(mins, secs)
            timer_label.config(text=time_format)
            timer_label.master.after(1000, countdown, count-1)
        else:
            timer_label.master.configure(background='navy')
            for widget in timer_label.master.winfo_children():
                widget.pack_forget()
            end_button = tk.Button(timer_label.master, text="休憩終了", command=lambda: destroy_all_windows(roots), font=("Helvetica", 24))
            end_button.pack(expand=True)

    countdown(duration_seconds)

def destroy_all_windows(roots):
    for root in roots:
        root.destroy()

if __name__ == "__main__":
    start_work_timer()