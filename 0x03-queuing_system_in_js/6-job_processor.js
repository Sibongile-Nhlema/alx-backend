const kue = require('kue');
const queue = kue.createQueue();

// Send notifications
function sendNotification(phoneNumber, message) {
  console.log(`Sending notification to ${phoneNumber}, with message: ${message}`);
}

// Process jobs from the 'push_notification_code' queue
queue.process('push_notification_code', (job, done) => {
  const { phoneNumber, message } = job.data;

  sendNotification(phoneNumber, message);

  done();
});

// Log when the job is finished
queue.on('job complete', (id, result) => {
  console.log(`Job ${id} completed`);
});

// Log when the job is not successful
queue.on('job failed', (id, errorMessage) => {
  console.error(`Job ${id} failed: ${errorMessage}`);
});