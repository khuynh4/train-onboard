import './App.css';
import React from 'react';
import { Header } from './Comps/header.jsx';
import {
  BrowserRouter as Router,
  Switch,
  Route,
  Redirect
} from "react-router-dom";
import { Home } from './Comps/home.jsx';
import { TraineeLayout } from './Layouts/traineeLayout.jsx';
import { Navigation } from "./Comps/Navbars/TraineeNavbar.jsx";
import { HomeNavbar } from "./Comps/Navbars/HomeNavbar.jsx";
import "bootstrap/dist/css/bootstrap.min.css";
import { TraineeDashboard } from "./Views/TraineeDashboard.jsx"
import { Sidebar } from "./Comps/Sidebars/TraineeSidebar.jsx";
import { Login } from "./Comps/Authentication/login.jsx";
import { Signup } from "./Comps/Authentication/signup.jsx";

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
          <Switch>
            <Route exact path="/">
              <HomeNavbar />
              <Home />
            </Route>
            <Route path="/login">
              <HomeNavbar />
              <Login onLogin={ this.onLogin } onLoginError={ this.onLoginError }/>
            </Route>
            <Route path="/signup">
              <HomeNavbar />
              <Signup />
            </Route>
            <Route path="/user">
              <TraineeLayout name={ this.state.name } onLogout={ this.onLogout }/>
            </Route>
          </Switch>
        </Router>
      );
    }
}

export default App;
