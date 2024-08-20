import tkinter as tk
import math

def show_heart():
    heart_window = tk.Toplevel(root)
    heart_window.title("Heart")

    canvas = tk.Canvas(heart_window, width=400, height=400, bg="white")
    canvas.pack()

    texts = ["Tiako enao", "I love you", "Je t'aime"]
    text_index = 0

    def heart_shape(t, scale=1):
        x = 16 * (math.sin(t) ** 3)
        y = 13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t)
        return scale * x, scale * y

    def draw_heart(offset_x=0, broken=True, scale=1):
        canvas.delete("all")

        # Dessiner le cœur avec des dégradés pour l'effet 3D
        num_layers = 20
        for i in range(num_layers):
            layer_scale = scale * (1 - 0.05 * i)
            color_value = 255 - int(255 * (i / num_layers))
            color = f'#{color_value:02x}0000'

            left_points = []
            right_points = []
            for t in range(0, 360):
                angle = math.radians(t)
                x, y = heart_shape(angle, layer_scale)
                if x < 0:
                    left_points.append((200 + 10 * x - offset_x, 200 - 10 * y))
                else:
                    right_points.append((200 + 10 * x + offset_x, 200 - 10 * y))

            canvas.create_polygon(left_points + right_points[::-1], fill=color, outline="")

        # Dessiner le cœur principal
        left_points = []
        right_points = []
        for t in range(0, 360):
            angle = math.radians(t)
            x, y = heart_shape(angle, scale)
            if x < 0:
                left_points.append((200 + 10 * x - offset_x, 200 - 10 * y))
            else:
                right_points.append((200 + 10 * x + offset_x, 200 - 10 * y))

        if broken:
            for i in range(len(left_points) - 1):
                canvas.create_line(left_points[i], left_points[i + 1], fill="red", width=2)
            for i in range(len(right_points) - 1):
                canvas.create_line(right_points[i], right_points[i + 1], fill="red", width=2)
        else:
            canvas.create_polygon(left_points + right_points[::-1], fill="red", outline="red")
            text = texts[text_index % len(texts)]
            canvas.create_text(200, 200, text=text, fill="white", font=("Helvetica", 24, "bold"), justify="center")

    def animate_heart():
        offset_x = 100
        direction = -1

        def update():
            nonlocal offset_x, direction
            if offset_x <= 0:
                direction = 0  # Stop moving when the heart is united
                beat_heart()
                return

            offset_x += direction * 2
            draw_heart(offset_x, broken=True)
            if direction != 0:
                heart_window.after(30, update)

        update()

    def beat_heart():
        scale = 1
        direction = 1
        nonlocal text_index

        def update_beat():
            nonlocal scale, direction, text_index
            if scale >= 1.2:
                direction = -1
                text_index += 1
            elif scale <= 1:
                direction = 1

            scale += direction * 0.02
            draw_heart(broken=False, scale=scale)
            heart_window.after(100, update_beat)

        update_beat()

    animate_heart()

root = tk.Tk()
root.title("Love Message")

love_button = tk.Button(root, text="Click me", command=show_heart, font=("Helvetica", 18))
love_button.pack(pady=20)

root.mainloop()
