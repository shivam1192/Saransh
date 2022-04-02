import React from 'react';
import {Navbar,Nav} from 'react-bootstrap'

const NavBar = () => {
  
    return ( 
        <>
            <Navbar style={{backgroundColor:'#4c7a9c'}} collapseOnSelect fixed="top" expand="lg">
                <Navbar.Brand href="/" style={{color:"white"}}>Saransh</Navbar.Brand>
                <Navbar.Toggle aria-controls="responsive-navbar-nav" />
                <Navbar.Collapse id="responsive-navbar-nav">
                    <Nav className="mr-auto"></Nav>
                    <Nav>
                    </Nav>
                </Navbar.Collapse>
                </Navbar>
        </>
     );
}
 
export default NavBar;