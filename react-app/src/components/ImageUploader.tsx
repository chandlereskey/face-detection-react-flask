import { ReactHTMLElement, useEffect, useState } from "react";

export default function ImageUploader() {
  const [images, setImages] = useState<FormData>();
  useEffect(() => {
    // make api call to backend and pass in the images list and generate the txt file that will be used for face detection
    fetch("http://127.0.0.1:5001/generate_embeddings", {
      method: "POST",
      body: images,
    });
    console.log("images", images);
  }, [images]);

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event?.target?.files) {
      const tempArray = new FormData();
      for (let i = 0; i < event.target.files.length; i++) {
        tempArray.append("images" + i, event.target.files[i]);
      }
      setImages(tempArray);
    }
  };

  return (
    <>
      <input
        type="file"
        multiple
        onChange={(event) => handleFileChange(event)}
      />
      {/* {images.map((image: File, index) => {
        return (
          <div>
            <div>Image Here</div>
            <img
              key={index}
              src={URL.createObjectURL(image)}
              alt={image.name}
            />
          </div>
        );
      })} */}
    </>
  );
}
