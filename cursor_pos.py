import win32api

flags, hcursor, (x,y) = win32api.GetCursorInfo()

print(f"flags={flags}")
print(f"x,y = {x},{y}")
print(f"hcursor={hcursor}")


