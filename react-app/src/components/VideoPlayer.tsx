import React, { useRef, useEffect, useState, useCallback } from "react";
import Webcam from "react-webcam";

const VideoPlayer: React.FC = () => {
  const webcamRef = useRef<Webcam>(null);
  const [imageSrc, setImageSrc] = useState<string>("");

  const capture = useCallback(async () => {
    const imageSrc = webcamRef.current?.getScreenshot();
    if (imageSrc) {
      try {
        const response = await fetch(
          "http://127.0.0.1:5001/video-stream-from-flask-example",
          {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({ image: imageSrc }),
          }
        );
        const data = await response.json();
        setImageSrc(data.image); // Assuming the backend returns the processed image URL
      } catch (error) {
        console.error("Error sending video feed:", error);
      }
    }
  }, []);

  useEffect(() => {
    const interval = setInterval(capture, 1000 / 30); // Capture at 30 FPS
    return () => clearInterval(interval);
  }, [capture]);

  return (
    <div>
      <Webcam
        audio={false}
        ref={webcamRef}
        screenshotFormat="image/jpeg"
        width={640}
        height={480}
      />
      {imageSrc && <img src={imageSrc} alt="Processed video feed" />}
    </div>
  );
};

export default VideoPlayer;
