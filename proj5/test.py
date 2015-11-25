#!/usr/bin/env python

"""
TODO
- Leaderboard output
- Tweak the pass/fail parameters as necessary
"""

from run import Simulation

def run_test(filename, description, requests, replicas, mayfail, tolerance, latency):
	sim = Simulation(filename)
	sim.run()
	stats = sim.get_stats()	
	
	pf = 'PASS'
	if stats.incorrect:
		print '\t\tTesting error: >0 incorrect responses to get()'
		pf = 'FAIL'
	elif stats.failed_get > requests * mayfail or stats.failed_put > requests * mayfail:
		print '\t\tTesting error: Too many type=fail responses to client requests'
		pf = 'FAIL'
	elif stats.total_msgs > requests * replicas * 2 * tolerance:
		print '\t\tTesting error: Too many total messages'
		pf = 'FAIL'
	elif stats.mean_latency > latency:
		print '\t\tTesting error: Latency of requests is too high'
		pf = 'FAIL'
	
	print '\t%-40s\t[%s]' % (description, pf)
	return pf == 'PASS'
	
trials = []
print 'Basic tests (5 replicas, 30 seconds, 500 requests):'
trials.append(run_test('simple-1.json', 'No drops, no failures, 80% read', 500.0, 5.0, 0.05, 1.2, 0.001))
trials.append(run_test('simple-2.json', 'No drops, no failures, 60% read', 500.0, 5.0, 0.05, 1.2, 0.001))
trials.append(run_test('simple-3.json', 'No drops, no failures, 40% read', 500.0, 5.0, 0.05, 1.2, 0.001))
trials.append(run_test('simple-4.json', 'No drops, no failures, 20% read', 500.0, 5.0, 0.05, 1.2, 0.001))

print 'Unreliable network tests (5 replicas, 30 seconds, 500 requests):'
trials.append(run_test('unreliable-1.json', '10% drops, no failures, 80% read', 500.0, 5.0, 0.05, 1.25, 0.001))
trials.append(run_test('unreliable-2.json', '10% drops, no failures, 20% read', 500.0, 5.0, 0.05, 1.25, 0.001))
trials.append(run_test('unreliable-3.json', '20% drops, no failures, 80% read', 500.0, 5.0, 0.05, 1.3, 0.001))
trials.append(run_test('unreliable-4.json', '20% drops, no failures, 20% read', 500.0, 5.0, 0.05, 1.3, 0.001))
trials.append(run_test('unreliable-5.json', '30% drops, no failures, 80% read', 500.0, 5.0, 0.05, 1.35, 0.001))
trials.append(run_test('unreliable-6.json', '30% drops, no failures, 20% read', 500.0, 5.0, 0.05, 1.35, 0.001))

print 'Crash failure tests (5 replicas, 30 seconds, 500 requests):'
trials.append(run_test('crash-1.json', 'No drops, 1 replica failure, 80% read', 500.0, 5.0, 0.08, 1.3, 0.001))
trials.append(run_test('crash-2.json', 'No drops, 1 replica failure, 20% read', 500.0, 5.0, 0.08, 1.3, 0.001))
trials.append(run_test('crash-3.json', 'No drops, 2 replica failure, 80% read', 500.0, 5.0, 0.08, 1.3, 0.001))
trials.append(run_test('crash-4.json', 'No drops, 2 replica failure, 20% read', 500.0, 5.0, 0.08, 1.3, 0.001))
trials.append(run_test('crash-5.json', 'No drops, 1 leader failure, 80% read',  500.0, 5.0, 0.08, 1.3, 0.001))
trials.append(run_test('crash-6.json', 'No drops, 1 leader failure, 20% read',  500.0, 5.0, 0.08, 1.3, 0.001))

print 'Bring the pain (5 replicas, 30 seconds, 1000 requests):'
trials.append(run_test('advanced-1.json', '20% drops, 2 replica failure, 20% read', 1000.0, 5.0, 0.08, 1.3, 0.001))
trials.append(run_test('advanced-2.json', '30% drops, 2 replica failure, 20% read', 1000.0, 5.0, 0.08, 1.35, 0.001))
trials.append(run_test('advanced-3.json', '30% drops, 1 leader failure, 20% read',  1000.0, 5.0, 0.08, 1.35, 0.001))
trials.append(run_test('advanced-4.json', '50% drops, 2 leader failure, 20% read',  1000.0, 5.0, 0.08, 1.6, 0.001))

print 'Passed', sum([1 for x in trials if x]), 'out of', len(trials), 'tests'