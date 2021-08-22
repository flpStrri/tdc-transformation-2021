import http from 'k6/http';
import { check, sleep } from 'k6';

export let options = {
  stages: [
    { duration: '20s', target: 60 },
    { duration: '20s', target: 0 },
  ],
};

function get_foo(resource) {
  const res = http.get('http://127.0.0.1:3000/foos/' + resource);

  if (res.status !== 200) {
    console.log("status: ", res.status, " body: ", JSON.stringify(res.body))
  }
  return res;
}

export default function () {
  const resources = ['foo', 'bar', 'baz']
  const randomResource = resources[Math.floor(Math.random() * resources.length)];
  let res = get_foo(randomResource);
  check(res, { 'status was 200': (r) => r.status == 200 });
  sleep(Math.random());
}
