import './App.css';
import React, { useState } from 'react';
import { Header } from './Comps/header.jsx';
import {
  BrowserRouter as Router,
  Switch,
  Route,
  Link
} from "react-router-dom";

class App extends React.Component {

  constructor(props) {
      super(props);
      this.state = {
        isLoggedIn: false,
        access_token: '',
        uuid: '',
        name: '',
        email: ''
      };
  }

  onLogin = (data) => {
    this.setState({ 
      isLoggedIn: data.isLoggedIn,
      access_token: data.access_token,
      uuid: data.uuid,
      name: data.name,
      email: data.email
     });

     localStorage.setItem("user_data", JSON.stringify(this.state));
  }

  onSignup = (data) => {
    this.setState({
      isLoggedIn: data.isLoggedIn,
      access_token: data.access_token,
      uuid: data.uuid,
      name: data.name,
      email: data.email
    });

    localStorage.setItem("user_data", JSON.stringify(this.state));
  }

  onSignupError = (error) => {
    console.log(error);
    this.setState({ isLoggedIn: false});
  }

  onLogout = () => {
    localStorage.removeItem("user_data");
    this.setState({ isLoggedIn: false });
  }

  onLoginError = (error) => {
      console.log(error)
      this.setState({ isLoggedIn: false })
  }

  componentDidMount() {
    if (localStorage.getItem("user_data")) {
      this.setState(JSON.parse(localStorage.getItem("user_data")));
    }
  }

    render() {

      console.log(this.state);

      return (
          <Router>
            <div className="App">
              <Header isLoggedIn={ this.state.isLoggedIn } name={ this.state.name } onLogin={ this.onLogin } onSignup={ this.onSignup } onSignupError={ this.onSignupError }onLogout={ this.onLogout } onLoginError={this.onLoginError }/>
            </div>
          </Router>
      );
    }
}

export default App;
