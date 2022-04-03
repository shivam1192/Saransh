import React from 'react';
import { Button, Modal, Spinner } from 'react-bootstrap';
import VideoUpload from './videoUpload';

const ModalComp = (props) => {
    return ( 
        <>
             <Modal show={props.show} onHide={props.handleClose}>
                <Modal.Header closeButton>
                <Modal.Title>Upload Your Video</Modal.Title>
                </Modal.Header>
                <Modal.Body>Upload Your Video To Summarise the Video content in text format.</Modal.Body>
                <VideoUpload/>
                <Modal.Footer>
                <Button variant="secondary" onClick={props.handleClose}>
                    Close
                </Button>
                </Modal.Footer>
            </Modal>
        </>
     );
}
 
export default ModalComp;