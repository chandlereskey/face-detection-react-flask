import { useEffect, useState } from "react";
import { io, Socket } from "socket.io-client";
import Button from "./Button";
import Alert from "./components/Alert";
import Webcam from "react-webcam";
import ImageUploader from "./components/ImageUploader";
import VideoPlayer from "./components/VideoPlayer";

function App() {
  const [startVideo, setStartVideo] = useState(false);

  const handleStartConnection = () => {
    if (startVideo === false) {
      setStartVideo(true);
    } else {
      setStartVideo(false);
    }
  };

  return (
    <div>
      <ImageUploader />
      {startVideo && <VideoPlayer />}
      {/* <EstablishSocketConnection connect={startConnection} /> */}
      <button onClick={handleStartConnection}>
        {startVideo ? "Stop" : "Start"} Video With Face Detection
      </button>
    </div>
  );
}

export default App;
