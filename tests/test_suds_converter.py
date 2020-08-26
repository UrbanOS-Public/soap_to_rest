import pytest

from soap_to_rest.suds_converter import suds_to_serializable
from suds.sudsobject import Factory as SudsFactory

def test_single_primordial_value():
  assert [5] == suds_to_serializable(5)


def test_multiple_primordial_values():
  assert ['Hello', 'World'] == suds_to_serializable(['Hello', 'World'])


def test_single_regular_object():
  regular_object = RegularObject(
    'Jim Doe',
    '123 Front Street'
  )

  assert regular_object == suds_to_serializable(regular_object)


def test_single_suds_object():
  suds_object = SudsFactory.object(dict={
    'name': 'John Doe',
    'address': '123 Jump Street'
  })

  assert {'name': 'John Doe', 'address': '123 Jump Street'} == suds_to_serializable(suds_object)


def test_multiple_regular_objects():
  regular_objects = [
    RegularObject(
      'Jim Doe',
      '123 Front Street'
    ),
    RegularObject(
      'Billy Doe',
      '456 Front Street'
    )
  ]

  assert regular_objects == suds_to_serializable(regular_objects)


def test_multiple_suds_objects():
  suds_objects = SudsFactory.object(dict={
    'person': [
      SudsFactory.object(dict={
        'name': 'John Doe',
        'address': '123 Jump Street'
      }),
      SudsFactory.object(dict={
        'name': 'Jammy Doe',
        'address': '456 Jump Street'
      })
    ]
  })

  assert [
    {'name': 'John Doe', 'address': '123 Jump Street'},
    {'name': 'Jammy Doe', 'address': '456 Jump Street'}
  ] == suds_to_serializable(suds_objects)


def test_nested_suds_objects():
  suds_objects = SudsFactory.object(dict={
    'person': [
      SudsFactory.object(dict={
        'name': 'John Doe',
        'address': '123 Jump Street',
        'pets': SudsFactory.object(dict={
          'pet': [
            SudsFactory.object(dict={'name': 'Scrappy'})
          ]
        })
      }),
      SudsFactory.object(dict={
        'name': 'Jammy Doe',
        'address': '456 Jump Street',
        'pets': SudsFactory.object(dict={
          'pet': [
            SudsFactory.object(dict={'name': 'Bella'})
          ]
        })
      })
    ]
  })


def test_nested_mixed_objects():
  suds_objects = SudsFactory.object(dict={
    'person': [
      SudsFactory.object(dict={
        'name': 'John Doe',
        'address': '123 Jump Street',
        'pets': [
          SudsFactory.object(dict={'name': 'Scrappy'})
        ]
      }),
      SudsFactory.object(dict={
        'name': 'Jammy Doe',
        'address': '456 Jump Street',
        'pets': [
          SudsFactory.object(dict={'name': 'Bella'})
        ]
      })
    ]
  })

  assert [
    {'name': 'John Doe', 'address': '123 Jump Street', 'pets': [{'name': 'Scrappy'}]},
    {'name': 'Jammy Doe', 'address': '456 Jump Street', 'pets': [{'name': 'Bella'}]}
  ] == suds_to_serializable(suds_objects)

class RegularObject():
  def __init__(self, name, address):
    self.name = name
    self.address = address