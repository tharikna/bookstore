#!/usr/bin/env python3
import argparse
import json
import os

DATA_FILE = 'books.json'

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def create_book(title, author):
    data = load_data()
    book_id = max([b.get('id', 0) for b in data], default=0) + 1
    book = {'id': book_id, 'title': title, 'author': author}
    data.append(book)
    save_data(data)
    print(f'Created book with id {book_id}')

def list_books():
    data = load_data()
    if not data:
        print('No books found.')
    else:
        for b in data:
            print(f"{b['id']}: {b['title']} by {b['author']}")

def get_book(book_id):
    data = load_data()
    for b in data:
        if b.get('id') == book_id:
            print(json.dumps(b, indent=2))
            return
    print('Book not found.')

def update_book(book_id, title, author):
    data = load_data()
    for b in data:
        if b.get('id') == book_id:
            b['title'] = title
            b['author'] = author
            save_data(data)
            print('Book updated.')
            return
    print('Book not found.')

def delete_book(book_id):
    data = load_data()
    new_data = [b for b in data if b.get('id') != book_id]
    if len(new_data) == len(data):
        print('Book not found.')
    else:
        save_data(new_data)
        print('Book deleted.')

def main():
    parser = argparse.ArgumentParser(description='Bookstore CLI')
    subparsers = parser.add_subparsers(dest='command')

    create_parser = subparsers.add_parser('create', help='Create a new book')
    create_parser.add_argument('title')
    create_parser.add_argument('author')

    list_parser = subparsers.add_parser('list', help='List all books')

    read_parser = subparsers.add_parser('read', help='Read a book by id')
    read_parser.add_argument('id', type=int)

    update_parser = subparsers.add_parser('update', help='Update a book by id')
    update_parser.add_argument('id', type=int)
    update_parser.add_argument('title')
    update_parser.add_argument('author')

    delete_parser = subparsers.add_parser('delete', help='Delete a book by id')
    delete_parser.add_argument('id', type=int)

    args = parser.parse_args()

    if args.command == 'create':
        create_book(args.title, args.author)
    elif args.command == 'list':
        list_books()
    elif args.command == 'read':
        get_book(args.id)
    elif args.command == 'update':
        update_book(args.id, args.title, args.author)
    elif args.command == 'delete':
        delete_book(args.id)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
