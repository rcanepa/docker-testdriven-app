import React from 'react';

const AddUser = props => {
  return (
    <form action="">
      <div className="form-group">
        <input
          type="text"
          name="username"
          className="form-control input-lg"
          placeholder="Enter a username"
          required
        />
      </div>

      <div className="form-group">
        <input
          type="email"
          name="email"
          className="form-control input-lg"
          placeholder="Enter an email"
          required
        />
      </div>

      <div className="form-group">
        <input
          type="submit"
          value="submit"
          className="btn btn-primary btn-lg btn-block"
        />
      </div>
    </form>
  )
}

export default AddUser;