Single Department: Simple case with only one department. The aggregated score should be equal to the department's mean score.
Multiple Departments, Equal Importance: Two departments with equal importance should have their scores averaged equally.
Varying Importance: Tests the impact of department importance. The result should be weighted towards the more important department.
Outlier Department: Tests the impact of an outlier with a very high threat score. The result should not be overly skewed by the outlier.
Zero Users: Tests a department with zero users, which should not affect the aggregated score.
All Zero Scores: Tests when all departments have a mean score of zero. The result should be zero.
Large Sample Size: Tests with a large number of users to ensure the function handles large input correctly.
