point = -0.5
indexes = [0.0, -0.927, 24.59, -46.7, -11.75, 86.67, -38.1, -36.8, 24.0]
result = 0.0
for i in range(len(indexes)):
    print(i)
    result = result + indexes[i]*pow(point, i)

print(result)
print(result*200-100)