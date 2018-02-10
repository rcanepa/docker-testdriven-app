import React, { Component } from 'react';
import ReactDOM from 'react-dom';
import axios from 'axios';

import AddUser from './components/AddUser';
import UsersList from './components/UsersList';

class App extends Component {
  constructor() {
    super();
    this.addUser = this.addUser.bind(this);
    this.handleChange = this.handleChange.bind(this);
    this.state = {
      users: [],
      username: '',
      email: ''
    }
  }

  componentDidMount() {
    this.getUsers();
  }

  addUser(event) {
    event.preventDefault();
    const data = {
      username: this.state.username,
      email: this.state.email
    }
    axios.post(`${process.env.REACT_APP_USERS_SERVICE_URL}/users`, data)
      .then(res => {
        this.getUsers();
        this.setState({ username: '', email: '' });
      })
      .catch(err => console.log(err))
  }

  getUsers() {
    axios.get(`${process.env.REACT_APP_USERS_SERVICE_URL}/users`)
      .then(res => this.setState(() => ({ users: res.data.data.users })))
      .catch(err => console.log(err))
  }

  handleChange(event) {
    const obj = {};
    obj[event.target.name] = event.target.value;
    this.setState(() => (obj))
  }

  render() {
    return (
      <div className="container">
        <div className="row">
          <div className="col-md-4">
            <br />
            <h1>All Users</h1>
            <hr /><br />
            <AddUser
              addUser={this.addUser}
              username={this.state.username}
              email={this.state.email}
              handleChange={this.handleChange}
            />
            <br />
            <UsersList users={this.state.users} />
            <pre>
              {JSON.stringify(this.state.users, null, 2)}
            </pre>
          </div>
        </div>
      </div>
    )
  }
}


ReactDOM.render(
  <App />,
  document.getElementById('root')
);
