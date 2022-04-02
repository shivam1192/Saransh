import React, {useState} from 'react';
import { Button, Modal } from 'react-bootstrap';
import Home from '../home.png'
import NavBar from './navbar';
import ModalComp from './modal';



const MainHome = () => {
    const [show, setShow] = useState(false);

    const handleClose = () => setShow(false);
    const handleShow = () => setShow(true);
    return ( 
        <>
            <NavBar/>
            <div className="row">
                <div className="col-lg-4">
                    <h1 style={{ marginTop: '215px', fontSize: '97px', marginLeft: '78px', color: '#4c7a9c', fontFamily:'inherit'}} >Saransh</h1>
                    <span style={{    marginLeft: '76px', fontSize: '15px', color: '#eb842f'}}>Summarise your Video content in text format.</span><br/>
                    <span style={{    marginLeft: '76px', fontSize: '15px', color: '#eb842f'}}>Safely | Securely | Fastly</span><br/><br/>
                    <span style={{    marginLeft: '76px', fontSize: '15px'}}><Button variant="outline-secondary" onClick={handleShow}>Click to Summarise your Video</Button></span><br/>

                </div>
                <div className="col-lg-8" style={{marginTop:"70px"}}>
                <img src={Home} height="640"/>
                </div>
                <ModalComp show={show} handleClose={handleClose}/>
                </div>
        </>
     );
}
 
export default MainHome;