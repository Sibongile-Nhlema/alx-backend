import kue from 'kue';
import { expect } from 'chai';
import createPushNotificationsJobs from './8-job.js';

describe('createPushNotificationsJobs', () => {
  let queue;

  before(() => {
    // Create a queue and enter test mode
    queue = kue.createQueue();
    queue.testMode = true;
  });

  afterEach(() => {
    // Clear the queue after each test
    queue.testMode.jobs = [];
  });

  after(() => {
    // Exit test mode
    queue.testMode = false;
  });

  it('should display an error message if jobs is not an array', () => {
    expect(() => createPushNotificationsJobs({}, queue)).to.throw('Jobs is not an array');
  });

  it('should create jobs and log the correct messages', () => {
    const list = [
      {
        phoneNumber: '4153518780',
        message: 'This is the code 1234 to verify your account'
      },
      {
        phoneNumber: '4153518781',
        message: 'This is the code 4562 to verify your account'
      }
    ];

    createPushNotificationsJobs(list, queue);

    // Validate that jobs are inside the queue
    const jobs = queue.testMode.jobs;
    expect(jobs).to.have.lengthOf(2);

    const job1 = jobs[0];
    expect(job1.type).to.equal('push_notification_code_3');
    expect(job1.data).to.deep.equal(list[0]);

    const job2 = jobs[1];
    expect(job2.type).to.equal('push_notification_code_3');
    expect(job2.data).to.deep.equal(list[1]);
  });
});
