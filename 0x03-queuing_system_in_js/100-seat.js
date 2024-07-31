const express = require('express');
const redis = require('redis');
const kue = require('kue');
const { promisify } = require('util');
const app = express();
const port = 1245;
const client = redis.createClient();
const getAsync = promisify(client.get).bind(client);
const setAsync = promisify(client.set).bind(client);
const queue = kue.createQueue();

let reservationEnabled = true;

const initialSeats = 50;

setAsync('available_seats', initialSeats);

const reserveSeat = async (number) => {
  await setAsync('available_seats', number);
};

// Get current available seats
const getCurrentAvailableSeats = async () => {
  const seats = await getAsync('available_seats');
  return parseInt(seats, 10) || 0;
};

// Get available seats
app.get('/available_seats', async (req, res) => {
  const availableSeats = await getCurrentAvailableSeats();
  res.json({ numberOfAvailableSeats: availableSeats.toString() });
});

// Reserve a seat
app.get('/reserve_seat', async (req, res) => {
  if (!reservationEnabled) {
    return res.json({ status: 'Reservations are blocked' });
  }

  const job = queue.create('reserve_seat').save((err) => {
    if (err) {
      return res.json({ status: 'Reservation failed' });
    }
    res.json({ status: 'Reservation in process' });
  });
});

// Pocess the queue
app.get('/process', async (req, res) => {
  res.json({ status: 'Queue processing' });

  queue.process('reserve_seat', async (job, done) => {
    try {
      const availableSeats = await getCurrentAvailableSeats();
      if (availableSeats <= 0) {
        reservationEnabled = false;
        return done(new Error('Not enough seats available'));
      }

      await reserveSeat(availableSeats - 1);
      console.log(`Seat reservation job ${job.id} completed`);
      done();
    } catch (error) {
      console.log(`Seat reservation job ${job.id} failed: ${error.message}`);
      done(error);
    }
  });
});

app.listen(port, () => {
  console.log(`Server running on http://localhost:${port}`);
});