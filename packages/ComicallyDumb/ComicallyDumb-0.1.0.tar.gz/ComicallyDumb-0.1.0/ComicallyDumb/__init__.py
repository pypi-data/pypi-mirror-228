#python setup.py sdist bdist_wheel
#twine upload dist/*


class DumbRegression:
  def __init__(self, X, y):
    slope = 0
    for i in range(len(X)):
      for j in range(len(X)):
        if i == j:
          continue
        slope += (y[i]-y[j])/(X[i]-X[j])
    slope /= len(X)**2

    bias = sum(y)/len(X) - slope * sum(X)/len(X)
    
    self.slope, self.bias = slope, bias

