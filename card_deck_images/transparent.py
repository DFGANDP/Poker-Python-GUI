import cv2
import numpy as np

# Input image
input = cv2.imread('test_card1.jpg', cv2.IMREAD_COLOR)


# Convert to RGB with alpha channel
output = cv2.cvtColor(input, cv2.COLOR_BGR2BGRA)

# Color to make transparent
col = (106, 174, 105)

# Color tolerance
tol = (63, 40, 64)
#tol = (90, 60, 90)

# Temporary array (subtract color)
temp = np.subtract(input, col)

# Tolerance mask
mask = (np.abs(temp) <= tol)
mask = (mask[:, :, 0] & mask[:, :, 1] & mask[:, :, 2])

# Generate alpha channel
temp[temp < 0] = 0                                            # Remove negative values
alpha = (temp[:, :, 0] + temp[:, :, 1] + temp[:, :, 2]) / 3   # Generate mean gradient over all channels
alpha[mask] = alpha[mask] / np.max(alpha[mask]) * 255         # Gradual transparency within tolerance mask
alpha[~mask] = 255                                            # No transparency outside tolerance mask

# Set alpha channel in output
output[:, :, 3] = alpha

# Output images
#cv2.imshow("alpha", alpha)
cv2.imwrite('test_card1alpha.png', alpha)
cv2.imwrite('test_card1output.png', output)
#cv2.imshow("output", output)
cv2.waitKey(0)

cv2.destroyAllWindows()
