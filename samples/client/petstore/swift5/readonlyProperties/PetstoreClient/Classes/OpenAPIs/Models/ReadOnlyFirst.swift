//
// ReadOnlyFirst.swift
//
// Generated by openapi-generator
// https://openapi-generator.tech
//

import Foundation

public struct ReadOnlyFirst: Codable {

    public private(set) var bar: String?
    public private(set) var baz: String?

    public init(bar: String? = nil, baz: String? = nil) {
        self.bar = bar
        self.baz = baz
    }

}