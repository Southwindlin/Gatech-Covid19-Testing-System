module.exports = {
    HOST: "localhost",
    USER: "newuser",
    PASSWORD: "123123123",
    DB: "covidtest_fall2020",
    dialect: "mysql",
    pool: {
      max: 5,
      min: 0,
      acquire: 30000,
      idle: 10000
    }
  };