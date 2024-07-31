const kue = require('kue');
const queue = kue.createQueue();

// Array containing blacklisted phone numbers
const blacklistedNumbers = [
  '4153518780',
  '4153518781'
];

function sendNotification(phoneNumber, message, job, done) {
  job.progress(0, 100);

  // Check if phoneNumber is in the blacklisted array
  if (blacklistedNumbers.includes(phoneNumber)) {
    console.log(`Notification job #${job.id} failed: Phone number ${phoneNumber} is blacklisted`);
    return done(new Error(`Phone number ${phoneNumber} is blacklisted`));
  }

  // Simulate job processing
  setTimeout(() => {
    job.progress(50, 100);
    console.log(`Sending notification to ${phoneNumber}, with message: ${message}`);
    
    console.log(`Notification job #${job.id} completed`);
    done();
  }, 1000);
}

const jobQueue = kue.createQueue();

// Process jobs in the queue push_notification_code_2
jobQueue.process('push_notification_code_2', 2, (job, done) => {
  const { phoneNumber, message } = job.data;
  sendNotification(phoneNumber, message, job, done);
});

jobQueue.on('job enqueue', (id, type) => {
  console.log(`Notification job #${id} enqueued`);
});

jobQueue.on('job complete', (id, result) => {
  console.log(`Notification job #${id} completed`);
});

jobQueue.on('job failed', (id, error) => {
  console.log(`Notification job #${id} failed: ${error.message}`);
});

jobQueue.on('job progress', (id, progress) => {
  console.log(`Notification job #${id} ${progress}% complete`);
});
