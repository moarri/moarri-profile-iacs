

def draw_centered_string(graphics, xy, txt, color, fnt):
    if len(txt)>0:
        size = fnt.getsize(txt)
        graphics.text((xy[0] - int(size[0] / 2), xy[1] - int(size[1] / 2)), txt, fill=color, font=fnt)
