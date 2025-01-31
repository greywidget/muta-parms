# Mutable Parameters
Recently someone asked for help in our [Pybites Circle Community](https://pybites.circle.so/) with a [Python Bite](https://pybitesplatform.com) that seemed to be behaving unexpectedly.

It turned out that this was a result of modifying a mutable parameter passed to a function.  

For folks new to programming it is not obvious why modifying a variable inside a function might cause a change outside of that function. Let's have a closer look at the underlying issue.

## What is a Python Variable
When considering variables in Python it is a good idea to differentiate between a variable's name and the object that it represents.

```
>>> inspiration = None #1
>>> id(inspiration)
140713396607856
>>> inspiration = "Read Atomic Habits" #2
>>> id(inspiration)
3034242491760

>>> inspiration = "Bob and Julian" #3
>>> id(inspiration)
3034242497712

>>> nums = list(range(10))
>>> nums
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9] #4
>>> id(nums)
3034242497984
>>> nums.append(10)
>>> nums
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10] #5
>>> id(nums)
3034242497984

>>> me = "Tarzan"
>>> me_too = me
>>> id(me)
2546636178128
>>> id(me_too)
2546636178128
>>> me is me_too
True #6
```

1. The `inspiration` variable is pointing to the Singleton `None`
2. The `inspiration` variable is now pointing to a string
3. The `inspiration` variable is now pointing to a different string, and as strings are `immutable`, the `id` has changed. It's a different object.
4. The `nums` variable is pointing to a list
5. The list that `nums` is pointing to has been modified, but the `id` is the same because lists are `mutable`.
6. Variables `me` and `me_too` are *both* pointing to the same string.

## Python passes parameters by Reference
Python passes parameters to functions by Reference - also referred to as *call by sharing*. This results in multiple names bound to the same object.  

Consider this simple case where a global variable is passed into a function:

```
FAB_FOUR = ["John", "Paul", "George", "Ringo"] #1


def meet_the_beatles(members) -> None: #2
    members.sort() #3
    print(f"   ...  {members}")


def main():
    print(f"Before: {FAB_FOUR}")
    meet_the_beatles(FAB_FOUR)
    print(f" After: {FAB_FOUR}")


if __name__ == "__main__":
    main()
```
1. Our global variable
2. Our positional (mutable) parameter
3. Sorting our *local* variable

Running the above code results in the following output:
```
Before: ['John', 'Paul', 'George', 'Ringo']
   ...  ['George', 'John', 'Paul', 'Ringo']
 After: ['George', 'John', 'Paul', 'Ringo']
```

Which shows that our global variable FAB_FOUR has indeed been modified. This is because our function variable `members` is really just an alias for the global variable `FAB_FOUR` - they point to the same object. 

The excellent site [Python Tutor](https://pythontutor.com/) can be used to provide a nice visualisation:

![visual_1](visual_1.png)


## Take Care when programming with Mutable Parameters
Functions that mutate their input values or modify state in other parts of the program behind the scenes are said to have [side effects](https://en.wikipedia.org/wiki/Side_effect_(computer_science)) and as a general rule this is best avoided. However, it is not uncommon to encounter such behaviour in real-world applications and it something we need to be aware of.

At the very least, you should consider carefully whether the caller expects the argument to be changed.

If you want to protect your code from such *side effects*, consider using immutable types where possible/practical. 

If it is not clear to you whether it is safe to modify a passed mutable parameter - create a copy of the parameter and modify that instead. Comprehensions provide a nice pythonic way to create new objects as does the `copy` module with its `copy`, and `deepcopy` functions.


## Mutable Types as Parameter Defaults
Python allows us to provide default values for function parameters - making them optional.  

For example, when we call `members.sort()` in our code above, the `sort` method has an optional keyword argument `reverse` which defaults to `False`. We can pass it with the value `True` to override the default behaviour:

```
>>> FAB_FOUR = ["John", "Paul", "George", "Ringo"]
>>> FAB_FOUR.sort()
>>> FAB_FOUR
['George', 'John', 'Paul', 'Ringo']
>>> FAB_FOUR.sort(reverse=True)
>>> FAB_FOUR
['Ringo', 'Paul', 'John', 'George']
```
The default values are evaluated once, at the point of function definition in the defining scope.

Using a Mutable Type as a paramater default should be avoided if possible because it can lead to unexpected and inconsistent behaviour. Consider the following code:

```
def enroll_student(name, students=[]):
    students.append(name)
    return students


def main():
    print(enroll_student("Biffa"))
    print(enroll_student("Moose"))
    print(enroll_student("Cheeseman"))


if __name__ == "__main__":
    main()
```

Running this code produces the following output:
```
['Biffa']
['Biffa', 'Moose']
['Biffa', 'Moose', 'Cheeseman']
```
Our function seems to be retaining information from previous calls.

This is because default values are stored in function attribute `__defaults__` and if mutable, can be changed by the function code.

Lets modify our code to show this:
```
def enroll_student(name, students=[]):
    print(f"ID of students: {id(students)}")  #1
    students.append(name)
    return students


def main():
    enroll_student("Biffa")
    print(f"Function Default Values: {enroll_student.__defaults__}")  #2
    print(f"ID of default_students: {id(enroll_student.__defaults__[0])}")  #3


if __name__ == "__main__":
    main()
```
1. Print the `id` of local variable `students`
2. Print the `enroll_student` parameter default values
3. Print the `id` of `students` default value

Running this code produces the following output:
```
ID of students: 2667038141888
Function Default Values: (['Biffa'],)
ID of default_students: 2667038141888
```

This shows that our local `students` variable and its *default value* both point to the same object. Modifying the local variable will cause the default value to be updated on the function object!

To prevent this behaviour, we can specify `None` as the default value, and handle that case inside our code. `None` is immutable. Here is our new version of the function:

```
def enroll_student(name, students=None):
    if students is None:
        students = []
    students.append(name)
    return students
```

Looking at the output, we can see that the immutable `None` is stored as the function default for `students` and is no longer coupled to our local `students` variable:
```
ID of students: 1545913462208
Function Default Values: (None,)
ID of default_students: 140713967338128
```
And our code works consistently:

```
def main():
    print(enroll_student("Biffa"))
    print(enroll_student("Moose"))
    print(enroll_student("Cheeseman"))
```

Which produces:
```
['Biffa']
['Moose']
['Cheeseman']
```

