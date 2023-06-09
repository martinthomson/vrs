---
title: "A Verifiable Random Selection Process"
abbrev: "Verifiable Random Selection"
category: info

docname: draft-thomson-elegy-vrs-latest
submissiontype: IETF  # also: "independent", "IAB", or "IRTF"
number:
date:
consensus: true
v: 3
area: "General"
workgroup: "NomCom Eligibility Update"
keyword:
 - next generation
 - crypto
venue:
  group: "NomCom Eligibility Update"
  type: "Working Group"
  mail: "eligibility-discuss@ietf.org"
  arch: "https://mailarchive.ietf.org/arch/browse/eligibility-discuss/"
  github: "martinthomson/vrs"
  latest: "https://martinthomson.github.io/vrs/draft-thomson-elegy-vrs.html"

author:
 -
    fullname: Martin Thomson
    organization: Mozilla
    email: mt@lowentropy.net

normative:
  HKDF: RFC5869

informative:
  CSS3:
    title: "CSS Color Module Level 3"
    target: "https://www.w3.org/TR/2022/REC-css-color-3-20220118/"
    date: 2022-01-18
    seriesinfo:
      W3C: Recommendation
    author:
      - fullname: Tantek Çelik
      - fullname: Chris Lilley
      - fullname: L. David Baron


--- abstract

A process for performing random selection without bias is described.


--- middle

# Introduction


# Process

A random selection process might be invoked to select a subset of one or more
items from a longer list of options.  The purpose of this process is to select
uniformly at random with minimal risk that the selection is influenced by
anyone, including those responsible for executing the process.

This process does not describe how the list of options is assembled, only how a
random selection is made.

The process allows for there to be additional constraints on selection, as well
as providing process in case a selected option needs to be removed for
unexpected reasons.

The process for random selection is as follows:

1. Agree to use this process.  If this fails, abort.

2. Appoint a facilitator, who will execute the process.

3. The facilitator performs the following in any order:

   1. Publish the list of options, along with labels for each option; see
      {{labels}} for details.

   2. Choose and publish details for a source of randomness that will become
      available at some future time; see {{seeds}}.

   3. Generate and publish a one-time code; see {{otp}}.
   {: type="a"}

4. Wait for all randomness to become available.

5. Publish the next one-time code; see {{otp}}.

6. Generate a pseudorandom key by extracting randomness from the sources and the
   one-time code; see {{extract}}.

7. Run a pseudorandom function (PRF) using the generated key and taking each
   label as input; see {{expand}}.

8. Sort the output.

9. Perform selection.

Options are selected by taking from the sorted list in order, starting from the
value with the lowest lexical value.

There might be constraints on selection, such as requirements on diversity
within the final set or disqualifications.  If any option cannot be selected,
skip that option and select the next option from the list.  Options can only be
skipped as a result of known constraints on selection, disqualifications (as
below), and any factor that is not potentially subject to external influence.

Options might be disqualified for reasons that are unexpected or could be
subject to external influence, such as a volunteer becoming unavailable.  In
that case, the complete set of selections is produced, applying any constraints
as above.  After all selections are made, any unexpectedly unavailable options
are publicly noted as disqualified from selection and the process is iterated.

To select replacements for unexpectedly unavailable options, the process is
iterated from the key generation stage (Step 5 above), using the next one-time
code; see {{otp}}.  Using a one-time code avoids having to wait for new
randomness to become available, but might give the facilitator some influence
over the outcome; {{replacement}} explains in more detail.  Alternatively, the
entire process can be repeated.


## Labels {#labels}

Options require labels.  This process requires that each option be given a
unique and unambiguous label that is a sequence of bytes.

Labels could be anything, but using UTF-8 encoded strings {{?UTF8=RFC3269}}
without leading or trailing whitespace is ideal.  Such strings can be presented
in a text file or in the body of email announcements.

It should be clear what option each label corresponds to.  Names are often
excellent labels.  Any options have the same name can have extra text added to
disambiguate them.

The use of Unicode allows the possibility that some strings appear to be equal
when rendered, despite having very different character sequences.  Such
differences are significant; a single choice of encodingneeds to be made for
each label prior to the release of randomness.

The facilitator announces the set of labels that will be used prior to
any randomness being available.


## Randomness {#seeds}

A source of randomness needs to be chosen.  This source needs to produce
sufficient entropy both to ensure that all possible selection outcomes are
equally likely (see {{Section 3.3 of ?RFC3797}}) and to make pre-computation of
options infeasible (see {{security}}).

The randomness source might be assembled from multiple discrete sources.  Each
source and the date at which the entropy will be sampled needs to be announced.

A process for turning the randomness from each source into a single sequence of
bytes needs to be specified clearly.  This too should be announced.  {{Section 4
of ?RFC3797}} describes a method for the combination and canonical encoding of
multiple sources that each produce multiple integers.

Public lotteries are a good source of entropy, often providing in excess of 20
bits of entropy each.  Choosing three or four different lotteries likely
provides sufficient entropy.

The facilitator announces which lotteries are to be used, the date of the
lottery, and the encoding process.  This announcement needs to occur before any
of the lotteries are run.


## One-Time Codes {#otp}

A one-time code provides a facilitator with the ability to generate replacement
selections in case of unexpected unavailability of one or more options.

The facilitator selects a secret sequence of bytes.  This could be a string that
is UTF-8 encoded as is done for labels.

The facilitator then iteratively applies SHA-256
{{!SHA2=DOI.10.6028/NIST.FIPS.180-4}} to this sequence multiple times.  This
generates a hash commitment.  {{?RFC1760}} describes this process for use in
generating one-time passwords.

Concretely, if `H(secret)` is the process of hashing once, `H^2(secret) =
H(H(secret))` is hashing twice.  `H^n = H(H^{n-1}(secret))` is hashing `n`
times.

How many times the secret is hashed depends on the facilitators judgment of the
need to find replacements.  Hashing many more times than is expected to be
necessary will ensure that replacements can be produced immediately.

The facilitator publishes `H^n(secret)` and `n` prior to any randomness being
available.

Once randomness is available the first iteration of the selection process uses
`H^{n-1}(secret)`, or the preimage of the original published value.  In the
`i`-th iteration of the section process they use `H^{n-i}(secret)`, or the
preimage of the last published value.  At each iteration of the process, the
facilitator publishes the one-time code they use.

The chosen secret cannot be used.  If the process iterates enough times to reach
that point, new randomness and a new one-time code will need to be generated.

After the selection process is complete, the facilitator publishes their chosen
secret.


## Entropy Extraction {#extract}

Once randomness is available, the facilitator constructs a byte sequence from
the randomness as described in {{seeds}}.  They also obtain the one-time code as
described in {{otp}}.

The `HKDF-Extract` function ({{Section 2.2 of HKDF}}) with a hash function of
SHA-256 is used to extract entropy and produce a pseudorandom key (or PRK).  The
`salt` input is set to the butes of the one-time code, the input keying material
or `IKM` is set to the bytes from the randomness sources.

~~~ pseudocode
PRF = HKDF-Extract(salt=one-time-code, IKM=randomness)
~~~

This produces a `PRK` value.


## Pseudorandom Function {#expand}

The `HKDF-Extract` function ({{Section 2.3 of HKDF}}) with a hash function of
SHA-256 is used as a pseudorandom function.  The pseudorandom key input, `PRF`,
is taken from the previous step ({{extract}}); the label for each option is used
as the `info` input; and, the output length, `L`, is 32 (measured in bytes).

~~~ pseudocode
order = HKDF-Expand(PRK, info=label, L=32)
~~~

This produces a value, `order`, that can be sorted.


## Announcements and Timing

A facilitator needs to communicate clearly throughout the process.

Announcements regarding labels, randomness, and one-time codes -- including the
encoding of each -- need to be made prior to any randomness becoming available.
A single announcement for all of this information might be sufficient.

Once randomness is available, a single announcement can include the revealed
one-time code and the result of that iteration of selection.

For all announcements, allowing some time for validation and questions is
advisable.  If it takes time to confirm that an option is available for
selection, the next iteration of the process cannot be started until that time
passes.

When publishing values, the facilitator can use hexadecimal encoding to produce
text strings that might be easier to use.


## Encoding and Sorting

For the sorting and selection process, using hexadecimal strings might also help
simplify handling.  Hexadecimal strings sort identically to the underlying byte
sequence.  If the hexadecimal strings are printed one to a line, with the input
label (or name) after it on the same line, that can make it easier to identify
options in the sorted output.

The sample code in {{code}} uses this method.  It does not sort its output, as
that can be performed by a standard `sort` tool.


## Hash Function Choice

This process uses SHA-256 as its hash function for both one-time codes ({{otp}})
and the KDF (Sections {{<extract}} and {{<expand}}).  A different hash function
could be used, but then it would not be this process.


# Security Considerations {#security}

Low entropy randomness in a selection process could allow an attacker to compute
all possible outcomes.  Then, the attacker might be able to select options (or
labels for options) that improve the odds of an outcome favorable to them.
Given the use of one-time codes in this process, the only attacker who is in any
position to take advantage of this is the facilitator.

An appeals process or similar can help safeguard against a facilitator that
might be untrustworthy.


## Facilitators and Selecting Replacements {#replacement}

A facilitator has a limited ability to influence the selection process. This
influence depends on the facilitator being able to cause a selected option to
become disqualified somehow.

For example, if the process selects from volunteers for a task, the facilitator
might need to check that selected volunteers are available to perform that task.
A facilitator will know who will be selected as a replacement, if that becomes
necessary.  If the facilitator prefers that a replacement is selected, they
could attempt to force the use of a replacement, such as by not investing enough
effort in confirming availability.

This process is not robust against this attack; it depends on some amount of
trust in the facilitator.  If concerns exist about the impartiality of the
facilitator, the entire process can be re-run if an option becomes unavailable.
However, this adds another period of waiting for fresh randomness, which could
be too slow.  This is therefore a question of balancing a small dependency on
the facilitator against expedience.


## Secrecy for One-Time Codes

The facilitator needs to keep the value they choose for generating one-time
codes a secret until the process completes and all selections are made.

An attacker that obtains this secret -- or any unused one-time code -- gains the
foreknowledge available to the facilitator described in {{replacement}}.



# IANA Considerations

This document has no IANA actions.


--- back

# Sample Code {#code}

This section includes simple python code for running this process.  Separate
scripts exist for running selection ({{code-selection}}) and managing one-time
codes ({{code-otp}}).


## Selection

Values for the randomness and one-time code are provided as the first and second
arguments to the python script in {{code-selection}}, which implements steps 6
and 7 of the process in {{process}}.

~~~ python
{::include select.py}
~~~
{: #code-selection title="Implementation of Pseudorandomness"}

This script is intended to be used with a separate sorting tool as follows:

~~~
$ ./select.py "$randomness" "$otp" | sort
~~~


## One-Time Codes

The script in {{code-otp}} implements the generation of one-time codes from a
secret.

~~~ python
{::include otp.py}
~~~
{: #code-otp title="Implementation of the One-Time Codes"}

This script can also be used to verify the value revealed by the facilitator.
The value revealed by the facilitator at each iteration of the process can be
passed to this script, which should produce all previously revealed values.


# Example Usage

A committee is tasked with painting a building (which may or may not be a bike
shed) and have concluded that three different colors are needed for walls,
doors, and trim (eaves, gutters, and so forth).  They managed to agree that the
blue or anything close to blue was undesirable, but could not otherwise
agree. Ultimately the group agreed to follow a random selection process.

The list of color names from CSS level 3 {{CSS3}} was agreed as the basis for
selection, with "transparent", "grey", "cyan", and "magenta" being disqualifed
on the basis of either being not a color or an alias of another name.  A list of
those colors that were "blue" enough to be disqualified were agreed.

The facilitator chose a secret phrase "totally not a bikeshed", encoded it in
UTF-8, and published the output of 10 iterations of SHA-256 in hex:
950ea08d8d5fd3ae415b9967aba7a48aba39ca62a4d98f2e7fe25cb1b8f8c488.

The facilitator announced the exact process for public randomness, including the
use of three different lotteries on a future date and how the results would be
encoded, using the method from RFC 3797. After waiting, the lotteries finally
ran to produce the unlikely string of "1.2.3.4.5.6./1.2.3.4.5.6./1.2.3.4.5.6./".

The facilitator revealed the output of the 9th hash iteration
(5346f2efb5397a6788fc1f1d9c05c6d3f2abe9b7d16d8592a3695b6dbe9f2456) and ran the
selection process, producing the following (including only the first few lines,
with the hashes truncated for formatting reasons):

~~~
002ed527ae0a44a86c205d1cdba... lavenderblush
03f710be2b61a6f9c3f89aa5ab5... blue
08bab81380d7f0769cecf9969a8... darkgoldenrod
0c26494fa81f3aed8a9f66e77b7... mediumvioletred
0e1af5d1ccfd44de075cc0bb6d5... bisque
13a07cc9abf3b737e49a62b0634... lightpink
~~~

As blue was disqualified by prior agreement, the allocation was: walls
"lavenderblush", doors "darkgoldenrod", and trim "mediumvioletred".  However, upon an
attempt to acquire the "lavenderblush" paint, the supplier was unable to source
enough to cover the needed area; a replacement was needed.

The facilitator revealed the output of the 8th hash iteration
(2f70f884997ce80771adbefbbbc6c71a1b921da71896c25ca0f64966bfd0c8ce), producing:

~~~
00d1c59a9f1b581060a9e732e91... aqua
02b514b0b1807bfe086db524f40... darkgray
0337add95eac62a356b020a273a... cornflowerblue
~~~

The first option of "aqua" was selected for use on the walls. Concerns were
raised about "aqua" being basically blue and that it should have been
disqualified instead of "cyan", but the outcome of the process was not in
dispute as the qualified colors were very clearly specified as part of the
agreed process and that process had been strictly adhered to.

Only murmurs about the paint supplier's familial relationship with the
facilitator would mean that the color scheme did not last long, though maybe
that was a consquence of strident complaints from the neighbors.


# RFC 3797

This document describes what is an alternative process to that described in RFC
3797 {{?RFC3797}}.  It makes no effort to replace RFC 3797, however it is worth
noting certain key differences.

This process allows for more rapid replacement through the use of a one-time
code.

This process is marginally more robust against the inclusion of disqualified
options.  The process in RFC 3797 critically depends on the number of options
being known; see {{Section 5.1 of ?RFC3797}}, which recommends that invalid
options remain in the list after the list is determined.  This is because RFC
3797 selects from an ordered list by calculating an index from its PRF output,
modulo the number of remaining options.

In comparison, this process sorts the output of its PRF, with each output being
dependent only on the randomness and the label.  For the process in this
document, only labels need to be fixed prior to learning the randomness, not the
composition of the entire list of options.



# Acknowledgments
{:numbered="false"}

The basic underlying idea here comes from {{{Paul Hoffman}}}.  {{?RFC3797}} and
the one-time code idea are both the work of {{{Donald Eastlake}}}.
