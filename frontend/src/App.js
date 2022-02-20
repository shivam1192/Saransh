
import {useState} from 'react';
import storage from './firebase';
import { getStorage, ref, listAll,getDownloadURL } from "firebase/storage";

function App() {
const [video , setVideo] = useState('');

const temp = (folder) =>{
  
  var listRef =  ref(storage,folder)
  listAll(listRef)
  .then((res) => {
      console.log(res.items[res.items.length - 1]);
      getDownloadURL(res.items[0]).then((url)=>{
      console.log(url);
    });
  }).catch((error) => {
    // Uh-oh, an error occurred!
    console.log(error);
  }); 
}
const upload = ()=>{
  if(video == null)
    return;
  storage.ref(`/videos/${video.name}`).put(video)
  .on("state_changed" , alert("success") , alert);

  temp("videos/")
 
}
  
  return (
    <div className="App">
      <center>
      <input type="file" accept='video/*' onChange={(e)=>{setVideo(e.target.files[0])}}/>
      <button onClick={upload}>Upload</button>
      </center>
    </div>
  );
}
  
export default App;