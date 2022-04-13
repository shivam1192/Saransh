import React from 'react';
import {useState} from 'react';
import storage from '../firebase';
import { getStorage, ref, listAll,getDownloadURL } from "firebase/storage";
import { Button, Spinner } from 'react-bootstrap';
import Icon from '../icons8-ok.svg'
import { saveAs } from "file-saver";


const VideoUpload = () => {
const [video , setVideo] = useState('');
const [show,setShow] = useState(false)
const [videoUpload,setVideoUpload] = useState(false)
const [loadingVideoToAudio,setLoadingVideoToAudio] = useState(false)
const [loadingAudioToText,setLoadingAudioToText] = useState(false)
const [loadingTextToSummary,setLoadingTextToSummary] = useState(false)
const [download,setDownload] = useState(false)
const [link,setLink] = useState()

const saveFile = () => {
  saveAs(
    link,
    "subtitle_summarisation.pdf"
  );
};
const temp = (folder) =>{
    setVideoUpload(false)
  var listRef =  ref(storage,folder)
  listAll(listRef)
  .then((res) => {
      console.log(res.items[res.items.length - 1]);
      getDownloadURL(res.items[0]).then((url)=>{
        console.log(url);
        fetch(`http://127.0.0.1:5000/flask/videotoaudio?videolink=${url}`)
        .then((response) => response.json())
        .then((actualData) =>{
            setLoadingVideoToAudio(false)
          fetch(`http://127.0.0.1:5000/flask/audiototext?audiolink=${actualData.data_link}`)
          .then((response) => response.json())
          .then((actualData) =>{
            setLoadingAudioToText(false)
            console.log(actualData)
            fetch(`http://127.0.0.1:5000/flask/texttosummary?textlink=${actualData.data_link}`)
            .then((response) => response.json())
            .then((actualData) =>{
              setLink(actualData.data_link)
                setLoadingTextToSummary(false)
                setDownload(true)
              console.log(actualData)
            });
          });
        });
    });
  }).catch((error) => {
    // Uh-oh, an error occurred!
    console.log(error);
  }); 
}
const upload = ()=>{
  if(video == null)
    return;
    setShow(true)
    setVideoUpload(true)
    setLoadingVideoToAudio(true)
    setLoadingAudioToText(true)
    setLoadingTextToSummary(true)

  storage.ref(`/videos/${video.name}`).put(video)
  .on("state_changed" , alert("success") , alert);

  temp("videos/")
 
}
  
    return ( 
        <>
      <center>
      <input type="file" accept='video/*' onChange={(e)=>{setVideo(e.target.files[0])}}/>
      <Button variant="primary" onClick={upload}>Upload</Button>
      </center>
      {
        show ? <>
          <h5>
        {videoUpload ? <><Spinner animation="border" role="status">
            <span className="visually-hidden">Loading...</span>
            </Spinner> Your video is being upload in our cloud.</>
            : <><img src = {Icon}></img>Your video has been uploaded in our cloud.</>
        }
        </h5><br/>
        <h5>
        {loadingVideoToAudio ? <><Spinner animation="border" role="status">
            <span className="visually-hidden">Loading...</span>
            </Spinner> We are converting your video into audio format</>
            : <><img src = {Icon}></img>We are converting your video into audio format.</>
        }
        </h5><br/>
        <h5>
        {loadingAudioToText ? <><Spinner animation="border" role="status">
            <span className="visually-hidden">Loading...</span>
            </Spinner>We are converting your audio file into text format.</>
            : <><img src = {Icon}></img>We are converting your audio file into text format.</>
        }
        </h5><br/>
        <h5>
        {loadingTextToSummary ? <><Spinner animation="border" role="status">
            <span className="visually-hidden">Loading...</span>
            </Spinner> We are Summarising your text document.</>
            : <><img src = {Icon}></img>We are Summarising your text document.</>
        }
        </h5><br/>
           {
             download ? <Button onClick={saveFile}>Download</Button> :null
           }   
        </> : null
      }
      </>
     );
}
 
export default VideoUpload;