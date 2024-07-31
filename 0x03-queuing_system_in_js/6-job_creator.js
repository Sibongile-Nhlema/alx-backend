const kue = require('kue');
const queue = kue.createQueue();

const jobData = {
  phoneNumber: '123-456-7890',
  message: 'Hello, this is a test notification!'
};

const job = queue.create('push_notification_code', jobData)
  .save((err) => {
    if (err) {
      console.error('Error creating job:', err);
    } else {
      console.log(`Notification job created: ${job.id}`);
    }
  });

// Event listeners for job status changes
job.on('complete', () => {
  console.log('Notification job completed');
});

job.on('failed', (errorMessage) => {
  console.error('Notification job failed:', errorMessage);
});