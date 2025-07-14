// src/components/NavBar.jsx

import Container from "react-bootstrap/Container";
import Nav from "react-bootstrap/Nav";
import Navbar from "react-bootstrap/Navbar";
import { Link } from "react-router-dom";
import 'bootstrap/dist/css/bootstrap.min.css';

function NavBar() {
  return (
    <Navbar expand="lg" bg="light" className="shadow-sm mb-4">
      <Container>
        <Navbar.Brand as={Link} to="/">🤖 Chatbot</Navbar.Brand>
        <Navbar.Toggle aria-controls="main-navbar" />
        <Navbar.Collapse id="main-navbar">
          <Nav className="me-auto">
            <Nav.Link as={Link} to="/">Home</Nav.Link>
            <Nav.Link as={Link} to="/chat">Chat</Nav.Link>
          </Nav>
        </Navbar.Collapse>
      </Container>
    </Navbar>
  );
}

export default NavBar;
