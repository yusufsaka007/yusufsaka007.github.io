---
title: "Advanced GraphQL Attacks: Part 1"
date: 2026-03-26
draft: false
tags: ["graphql", "api", "bola", "bug-bounty", "mobile", "authorization"]
---

Recently I got interested in API hacking, seeing during my tests more and more companies transforming their architectures from monolithic design to microservices. In this first part of my GraphQL hacking series you will get an introduction on what GraphQL is, and at the end I will show a critical finding I found regarding the GraphQL API of Belgian train company NMBS/SNCB.

## What Are APIs

Being in this field it's impossible to not be aware of APIs unless one lives under a rock.

An API, which stands for Application Programming Interface, is a technology that allows different software systems to communicate and transfer data with each other. It is especially useful when one wants data transfer between components with different languages or architectures. Think of it as a waiter in your local restaurant, being a bridge of communication between customers and the chefs.

There are multiple implementations of APIs.

We have the default standard REST (Representational State Transfer) with a simple CRUD style integration. Then there is the legacy SOAP (though it can still be seen in the wild, especially with telecom companies) and then there is *GraphQL*, which is becoming more and more popular among developers building complex frontend or mobile applications.

*GraphQL* is an API query language created originally by Facebook, designed to facilitate efficient communication between clients and servers. The difference between *GraphQL* and other API implementations is that with GraphQL the client doesn't have to know where different resources are located. All GraphQL requests are done on one endpoint, giving developers a tremendous amount of flexibility. However, this flexibility is not only in the favour of developers but also for us as hackers. In this blog post I share insights on how GraphQL works, what common vulnerabilities hunters should look for, tips and tricks on integrating Burp Suite with GraphQL, tooling, and so on. All the techniques will be showcased on [Damn Vulnerable GraphQL Application (DVGA)](https://github.com/dolevf/Damn-Vulnerable-GraphQL-Application). Credits to [the creator and contributors](https://github.com/dolevf/Damn-Vulnerable-GraphQL-Application/graphs/contributors) for creating this amazing lab allowing us hunters to interact with this promising technology. I hope you enjoy.

![DVGA](/images/bug-bounty/advanced-graphql-part1/1dvga.png)

GraphQL allows an API consumer to request certain resources from the server without also receiving unnecessary data. This also reduces the chance of unnecessary information disclosure, unlike in badly designed REST applications.

Unlike in many REST applications where read operations usually happen through `GET`, creation through `POST`, update through `PUT`, and deletion through `DELETE`, in GraphQL (usually but not necessarily) all of these operations happen through a `POST` request to a single endpoint.

## GraphQL Schemas

A GraphQL schema represents the structure of the data being requested. An example schema defining a `User` object can be written as follows:

```graphql
type User {
    id: Int
    username: String
    email: String
}
```

GraphQL also allows developers to link different types of objects with each other. Let's say we also have another object called `PaymentInfo`:

```graphql
type PaymentInfo {
   id: Int
   card_no: String
}
```

One can easily link both by nesting one within another:

```graphql
type User {
    id: Int
    username: String
    email: String
    payment_info: PaymentInfo
}
```

This means when requesting a `User` object one can also query the associated payment information for that specific user. This is known as a *one-way link relationship*. The reverse is not necessarily true, meaning one cannot request the correlated `User` object just by querying a `PaymentInfo` object.

> There can be occurrences of two-way link relationships if the developers specifically also insert the `User` object into the `PaymentInfo` type schema. This often leads to Denial of Service (DoS) situations. More on that in later chapters.

Once the schema is defined, the API consumer can interact with the entries in the database using **Queries**. There are 3 possible operations:

- `Queries` are used for read-only operations and do not modify the data.
- `Mutations` are used for data manipulation like create, update, or delete.
- `Subscriptions` are an interesting one, allowing real-time communication with the application. They allow GraphQL to push data to the client when different events occur.

Before using queries the developer must implement the schema. As an example:

```graphql
type Query {
  users: [User]
}

schema {
  query: Query
}

query {
   users {
        username
        email
   }
}
```

The `users` query will allow the consumer to receive all usernames and emails of the application.

An advantage of using GraphQL is performance. GraphQL improves the speed of client-server interactions by saving the client from having to make multiple requests in order to retrieve the complete set of data it needs from an application.

## Authentication and Authorization Flaws

One of the most common vulnerabilities in GraphQL is broken authentication and authorization. Authentication and authorization are complex security controls in any API technology.

## Broken Object Level Authorization (BOLA) in NMBS/SNCB

One day I decided to take on a new challenge and instead of focusing on the web so much I decided to find vulnerabilities in a mobile asset. The Belgian train company [*NMBS/SNCB*](https://www.belgiantrain.be/nl/support/customer-service/responsible-disclosure) was the perfect target for this. Since it was a vulnerability disclosure program (VDP) it was expected to be less crowded, making it perfect for gaining some experience with mobile hacking. It was also located in Belgium and I used it quite often, so I knew the boundaries of the application.

I got my rooted Xiaomi and opened the application. I noticed there were different API calls and different domains in use for different functionalities.

So I started testing. Whenever I am looking for broken authorization bugs I like to create 2 different accounts so that I can confirm access from one to another.

Upon logging in, I realized the server was giving me a JSON Web Token (JWT). If you want to learn more about JWT attacks refer to this [writeup](https://yusufsaka007.github.io/ctf/htb-criticalops/).

![JWT token](/images/bug-bounty/advanced-graphql-part1/2jwt_token.png)

Going to the homepage I noticed it makes different API calls, and some of them were going to *https://mobile-bff-ticketing.api.belgiantrain.be/api/graphql*.

As usual I tried firing up an **Introspection query**, which was disabled as expected. I then tried to generate the whole API schema by bruteforcing the suggestions, which was disabled as well. More about these techniques in later chapters.

At this point I started testing the available endpoints that I was aware of to access my other account's data, but as expected almost all of them were validating the JWT token and returning a 401 Unauthorized. Except for one. They forgot to validate the **JWT** for the `getOrdersByCustomer` operation and I got access to the previous orders of my other account, which were empty.

```
POST /api/graphql HTTP/1.1
Host: mobile-bff-ticketing.api.belgiantrain.be
Jwt: [attacker's valid JWT]
Content-Type: application/json

{
  "operationName": "getOrdersByCustomer",
  "variables": {
    "customerId": "390965xx", // victim's customer ID
    "language": "en"
  },
  "query": "query getOrdersByCustomer(...) { ... }"
}
```

```json
<SNIP>
{
    "data": {
        "orders": [

        ]
    }
}
```

At this point I decided to run a quick **FFUF** scan to prove the impact. I created a short wordlist of customer IDs, fired up the tool, and started getting many hits disclosing sensitive information like first name, last name, birthdate, email, order ID, and so on.

![FFUF results](/images/bug-bounty/advanced-graphql-part1/3ffuf_results.png)

**NMBS/SNCB** fixed the bug quickly and were kind enough to offer me a spot on their wall of fame.

## Lessons Learned

Just because security checks are being performed on some endpoints doesn't mean all of them are secure.