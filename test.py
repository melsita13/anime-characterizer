from PIL import Image
from clip_embedder import get_image_embedding

img = Image.open("./test_images/naruto.jpeg")
embedding = get_image_embedding(img)
print(embedding.shape)  # should print: torch.Size([1, 512])
