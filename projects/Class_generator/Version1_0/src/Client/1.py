try:
	a = float("5")
	if a == int(a):
		a = int(a)
except Exception:
	a = "5"

print(a)

try:
	a = float("5.2")
	print(a)
	print(int(a))
	if a == int(a):
		a = int(a)
except Exception:
	a = "5"

print(a)


try:
	a = float("5.0")
	if a == int(a):
		a = int(a)
except Exception:
	a = "5"

print(a)