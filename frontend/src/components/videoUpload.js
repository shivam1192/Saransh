import React from 'react';
import {useState} from 'react';
import storage from '../firebase';
import { getStorage, ref, listAll,getDownloadURL } from "firebase/storage";
import { Button } from 'react-bootstrap';
const VideoUpload = () => {
    const [video , setVideo] = useState('');
const [loading,setLoading] = useState(false)
const temp = (folder) =>{
  
  var listRef =  ref(storage,folder)
  listAll(listRef)
  .then((res) => {
      console.log(res.items[res.items.length - 1]);
      getDownloadURL(res.items[0]).then((url)=>{
        console.log(url);
        fetch(`http://127.0.0.1:5000/flask/videotoaudio?videolink=${url}`)
        .then((response) => response.json())
        .then((actualData) =>{
          fetch(`http://127.0.0.1:5000/flask/audiototext?audiolink=${url}`)
          .then((response) => response.json())
          .then((actualData) =>{
            console.log(actualData)
            setLoading(false)
          });
          console.log(actualData)
          setLoading(false)
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
  setLoading(true)
  storage.ref(`/videos/${video.name}`).put(video)
  .on("state_changed" , alert("success") , alert);

  temp("videos/")
 
}
  
    return ( 
        <>
    {loading ? <>Loading..</> :<>
      <center>
      <input type="file" accept='video/*' onChange={(e)=>{setVideo(e.target.files[0])}}/>
      <Button variant="primary" onClick={upload}>Upload</Button>
      </center>
      </>}
        </>
     );
}
 
export default VideoUpload;